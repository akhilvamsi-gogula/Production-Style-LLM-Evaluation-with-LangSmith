#!/usr/bin/env python3
"""Tag and filter the uploaded LangSmith dataset to inspect performance by category."""

import os
import sys
from pathlib import Path

from langsmith import Client

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _env import load_project_env

load_project_env()

def main() -> None:
    print("=" * 60)
    print("Tag and Filter Dataset")
    print("=" * 60)

    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET_NAME", "support-qa-golden-dataset")

    try:
        dataset = client.read_dataset(dataset_name=dataset_name)
    except Exception:
        print(f"[ERROR] Dataset not found: {dataset_name}. Run upload_dataset.py first.")
        return

    all_examples = list(client.list_examples(dataset_id=dataset.id))
    print(f"\nDataset: {dataset_name}")
    print(f"Total examples: {len(all_examples)}")

    tag_index = {}
    for example in all_examples:
        tags = example.metadata.get("tags", []) if example.metadata else []
        for tag in tags:
            tag_index.setdefault(tag, []).append(example)

    print("\nTag distribution:")
    for tag, examples in sorted(tag_index.items(), key=lambda item: -len(item[1])):
        print(f"  {tag}: {len(examples)} examples")

    filter_tag = "edge-case"
    filtered = tag_index.get(filter_tag, [])

    print(f"\nFiltered by '{filter_tag}': {len(filtered)} examples")
    for example in filtered:
        question = example.inputs.get("question", "N/A")
        answer = example.outputs.get("answer", "N/A")
        print(f" Q: {question}")
        print(f" A: {answer[:60]}...")
        print()

    print("=" * 60)
    print("Filtering complete")
    print("=" * 60)

if __name__ == "__main__":
    main()