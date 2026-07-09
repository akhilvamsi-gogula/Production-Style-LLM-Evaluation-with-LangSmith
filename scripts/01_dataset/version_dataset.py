#!/usr/bin/env python3
"""
Dataset Versioning
Datasets evolve over time. Versioning lets you reproduce past results
and track improvements as you add new examples.
"""

import os
import sys
from pathlib import Path

from langsmith import Client

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _env import load_project_env

load_project_env()

def main():
    print("=" * 60)
    print("Dataset Versioning")
    print("=" * 60)

    client = Client()

    source_name = os.getenv("LANGSMITH_DATASET_NAME", "support-qa-golden-dataset")
    versioned_name = f"{source_name}-v2"

    try:
        source_dataset = client.read_dataset(dataset_name=source_name)
    except Exception:
        print(f"[ERROR] Source dataset not found: {source_name}. Run upload_dataset.py first.")
        return

    source_examples = list(client.list_examples(dataset_id=source_dataset.id))
    print(f"\nSource dataset: {source_name}")
    print(f"  Examples: {len(source_examples)}")

    try:
        existing = client.read_dataset(dataset_name=versioned_name)
        client.delete_dataset(dataset_id=existing.id)
        print(f" Removed existing: {versioned_name}")
    except Exception:
        pass

    v2_dataset = client.create_dataset(
        dataset_name=versioned_name,
        description="Golden dataset V2 - extended with new examples"
    )

    for ex in source_examples:
        client.create_example(
            inputs=ex.inputs,
            outputs=ex.outputs,
            metadata=ex.metadata,
            dataset_id=v2_dataset.id
        )

    print(f"\nCreated: {versioned_name}")
    print(f" Copied {len(source_examples)} examples from V1")

    # Add new examples mined from production logs
    new_examples = [
        {
            "inputs": {"question": "Tell me about your cheapest product"},
            "outputs": {"answer": "The GreenGrow Smart Planter at $59.99 is our most affordable item"},
            "metadata": {"tags": ["product", "easy", "factual", "v2-addition"]}
        },
        {
            "inputs": {"question": "Is the SmartHome Hub X compatible with non-smart devices?"},
            "outputs": {"answer": "The SmartHome Hub X requires WiFi-enabled smart devices. It is not compatible with traditional non-smart appliances."},
            "metadata": {"tags": ["product", "medium", "factual", "v2-addition"]}
        }
    ]

    for ex in new_examples:
        client.create_example(
            inputs=ex["inputs"],
            outputs=ex["outputs"],
            metadata=ex.get("metadata", {}),
            dataset_id=v2_dataset.id
        )

    v2_examples = list(client.list_examples(dataset_id=v2_dataset.id))

    print(f" Added {len(new_examples)} new examples")
    print(f" V2 total: {len(v2_examples)} examples")

    print("\n" + "=" * 60)
    print("Dataset Versions:")
    print("=" * 60)
    print(f"\n V1: {source_name}")
    print(f"   {len(source_examples)} examples")
    print(f"\n V2: {versioned_name}")
    print(f"   {len(v2_examples)} examples ({len(new_examples)} new)")
    print(f"\nBoth versions exist independently in LangSmith.")

if __name__ == "__main__":
    main()