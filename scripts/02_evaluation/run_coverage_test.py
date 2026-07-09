#!/usr/bin/env python3
"""
Coverage Test - Run Experiment and Find Gaps
Run your Q&A pipeline against the golden dataset and analyze which
categories score lowest to identify coverage gaps.
"""

import os
import json
import sys
from pathlib import Path

from langsmith import Client
from langsmith.evaluation import evaluate

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "00_setup"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from create_keyword_evaluator import keyword_evaluator
from build_qa_pipeline import get_qa_pipeline
from _env import load_project_env

load_project_env()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent.parent / "data"

def exact_match_evaluator(run, example):
    prediction = run.outputs.get("output", "")
    reference = example.outputs.get("answer", "")
    score = 1.0 if prediction.strip().lower() == reference.strip().lower() else 0.0
    return {"key": "exact_match", "score": score}

def contains_evaluator(run, example):
    prediction = run.outputs.get("output", "")
    reference = example.outputs.get("answer", "")
    score = 1.0 if reference.strip().lower() in prediction.strip().lower() else 0.0
    return {"key": "contains_match", "score": score}

def main():
    print("=" * 60)
    print("Coverage Test - Run Experiment and Find Gaps")
    print("=" * 60)

    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET_NAME", "support-qa-golden-dataset")

    try:
        client.read_dataset(dataset_name=dataset_name)
    except Exception:
        print("[ERROR] Dataset not found. Run upload_dataset.py first.")
        return

    with open(DATA_DIR / "golden_dataset.json") as f:
        local_examples = json.load(f)

    print(f"\nDataset: {dataset_name}")
    print(f"Examples: {len(local_examples)}")

    qa_pipeline, _ = get_qa_pipeline("prompt_v1.txt")

    print("\nRunning coverage test evaluation...")
    # Return results object to analyze specific coverage misses
    results = evaluate(
        qa_pipeline,
        data=dataset_name,
        evaluators=[exact_match_evaluator, contains_evaluator, keyword_evaluator],
        experiment_prefix="coverage-test"
    )

    category_counts = {}
    for ex in local_examples:
        tags = ex.get("metadata", {}).get("tags", [])
        # Find the primary category tag (ignoring 'hard', 'easy', etc)
        category = next((t for t in tags if t in ["policy", "product", "edge-case", "adversarial"]), "untagged")
        category_counts[category] = category_counts.get(category, 0) + 1

    print("\n" + "=" * 60)
    print("Coverage Analysis by Category:")
    print("=" * 60)

    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {category.capitalize()}: {count} examples")

    print("\nLook for categories like 'edge-case' or 'adversarial' in your dashboard.")
    print("Those typically score lowest and represent your coverage gaps.")

if __name__ == "__main__":
    main()