#!/usr/bin/env python3
"""Upload the golden dataset to LangSmith so it can be used for experiments."""

import json
import os
import sys
from pathlib import Path

from langsmith import Client

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _env import load_project_env

load_project_env()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent.parent / "data"

def main() -> None:
    print("=" * 60)
    print("Upload Dataset to LangSmith")
    print("=" * 60)

    dataset_path = DATA_DIR / "golden_dataset.json"
    if not dataset_path.exists():
        print("[ERROR] golden_dataset.json not found. Run build_dataset.py first.")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        examples = json.load(f)

    print(f"\nLoaded golden dataset: {len(examples)} examples")

    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET_NAME", "support-qa-golden-dataset")

    try:
        existing = client.read_dataset(dataset_name=dataset_name)
        client.delete_dataset(dataset_id=existing.id)
        print(f" Removed existing dataset: {dataset_name}")
    except Exception:
        pass

    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Golden dataset for support QA evaluation"
    )
    print(f" Created dataset: {dataset_name}")

    for example in examples:
        client.create_example(
            inputs=example["inputs"],
            outputs=example["outputs"],
            metadata=example.get("metadata", {}),
            dataset_id=dataset.id,
        )

    uploaded = list(client.list_examples(dataset_id=dataset.id))
    print(f" Added {len(uploaded)} examples to dataset")
    
    print("\nVerify in LangSmith:")
    print("https://smith.langchain.com/ -> Click 'Datasets & Experiments'")

    print("\n" + "=" * 60)
    print("Dataset upload complete")
    print("=" * 60)

if __name__ == "__main__":
    main()