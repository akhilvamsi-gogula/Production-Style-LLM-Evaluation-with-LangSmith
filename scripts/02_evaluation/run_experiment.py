#!/usr/bin/env python3
"""Run a full LangSmith evaluation experiment for the prototype QA pipeline."""

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
    print("Run Evaluation Experiment (V1)")
    print("=" * 60)

    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET_NAME", "support-qa-golden-dataset")

    try:
        client.read_dataset(dataset_name=dataset_name)
    except Exception:
        print(f"[ERROR] Dataset {dataset_name} not found. Run upload_dataset.py first.")
        return

    # Build the pipeline
    qa_pipeline, _ = get_qa_pipeline("prompt_v1.txt")
    evaluators = [keyword_evaluator, llm_judge_evaluator]

    print("\nRunning experiment (this may take a minute)...")
    evaluate(
        qa_pipeline,
        data=dataset_name,
        evaluators=evaluators,
        experiment_prefix="qa-pipeline-v1",
    )

    project = os.getenv("LANGCHAIN_PROJECT", "default")
    print("\nExperiment complete!")
    print("\nCheck your LangSmith dashboard for detailed results:")
    print(f"https://smith.langchain.com/o/default/datasets?project={project}")

if __name__ == "__main__":
    main()