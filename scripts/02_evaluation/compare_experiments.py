#!/usr/bin/env python3
"""Run a second experiment with an improved prompt and compare it with the first."""

import os
import sys
from pathlib import Path

from langsmith import Client
from langsmith.evaluation import evaluate

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "00_setup"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from create_keyword_evaluator import keyword_evaluator
from create_llm_judge import llm_judge_evaluator
from build_qa_pipeline import get_qa_pipeline
from _env import load_project_env

load_project_env()

def main() -> None:
    print("=" * 60)
    print("Compare Experiments (V1 vs V2)")
    print("=" * 60)

    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET_NAME", "support-qa-golden-dataset")

    try:
        client.read_dataset(dataset_name=dataset_name)
    except Exception:
        print(f"[ERROR] Dataset not found: {dataset_name}. Run upload_dataset.py first.")
        return

    qa_pipeline_v2, v2_prompt = get_qa_pipeline("prompt_v2.txt")

    print(f"\nLoaded improved V2 prompt:\n  {v2_prompt[:80]}...")

    print("\nRunning V2 experiment...")
    evaluate(
        qa_pipeline_v2,
        data=dataset_name,
        evaluators=[keyword_evaluator, llm_judge_evaluator],
        experiment_prefix="qa-pipeline-v2"
    )

    project = os.getenv("LANGCHAIN_PROJECT", "default")
    print("\nExperiment comparison ready")
    print(f"\nOpen LangSmith to compare V1 and V2 side-by-side:")
    print(f"https://smith.langchain.com/o/default/datasets?project={project}")

if __name__ == "__main__":
    main()