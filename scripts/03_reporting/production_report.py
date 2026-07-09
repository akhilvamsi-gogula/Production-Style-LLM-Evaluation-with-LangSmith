#!/usr/bin/env python3
"""Generate a production-readiness report from the evaluation experiment results."""

import os
import sys
from pathlib import Path

from langsmith import Client
from langsmith.evaluation import evaluate

# Always go up 3 levels to the repo root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from _env import load_project_env
load_project_env()

# Import from scripts/00_setup/
sys.path.insert(0, str(ROOT_DIR / "scripts" / "00_setup"))
from create_keyword_evaluator import keyword_evaluator
from create_llm_judge import llm_judge_evaluator

# Import from scripts/02_evaluation/
sys.path.insert(0, str(ROOT_DIR / "scripts" / "02_evaluation"))
from build_qa_pipeline import get_qa_pipeline

def main() -> None:
    print("=" * 60)
    print("Production Readiness Report")
    print("=" * 60)

    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET_NAME", "support-qa-golden-dataset")

    try:
        client.read_dataset(dataset_name=dataset_name)
    except Exception:
        print(f"[ERROR] Dataset not found: {dataset_name}. Run upload_dataset.py first.")
        return

    # Use the improved V2 pipeline for the final check
    qa_pipeline, _ = get_qa_pipeline("prompt_v2.txt")

    thresholds = {
        "keyword_coverage": 0.6,
        "helpfulness": 0.7,
    }

    print("\nRunning production readiness evaluation...")
    experiment_prefix = "production-readiness"
    
    results = evaluate(
        qa_pipeline,
        data=dataset_name,
        evaluators=[keyword_evaluator, llm_judge_evaluator],
        experiment_prefix=experiment_prefix,
        max_concurrency=1  # Prevents Groq 429 Rate Limit error
    )
    
    experiment_name = results.experiment_name
    
    print("\nFetching aggregate metrics from LangSmith...")
    project_stats = client.read_project(project_name=experiment_name, include_stats=True)
    feedback_stats = project_stats.feedback_stats or {}
    
    avg_keyword = feedback_stats.get("keyword_coverage", {}).get("avg", 0.0)
    avg_helpfulness = feedback_stats.get("helpfulness", {}).get("avg", 0.0)

    print("\n" + "=" * 60)
    print(" PRODUCTION READINESS REPORT")
    print("=" * 60)

    metrics = {
        "keyword_coverage": avg_keyword,
        "helpfulness": avg_helpfulness,
    }

    all_pass = True
    for metric_name, score in metrics.items():
        threshold = thresholds.get(metric_name, 0)
        status = "PASS" if score >= threshold else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f" {metric_name:20s} | Score: {score:.2f} | Threshold: {threshold:.2f} | {status}")

    print("\n" + "-" * 60)
    if all_pass:
        print(" RECOMMENDATION: GO FOR PRODUCTION")
    else:
        print(" RECOMMENDATION: NOT READY - Fix failing metrics")
    print("=" * 60)

if __name__ == "__main__":
    main()