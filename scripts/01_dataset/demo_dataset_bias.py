#!/usr/bin/env python3
"""
Demonstrate the difference between a biased dataset and a robust golden dataset.
Highlights why diversity and edge-cases matter in LLM evaluation.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent.parent / "data"

def analyze_dataset(name, filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
        
    questions = [ex["inputs"]["question"] for ex in data]
    unique_questions = set(questions)
    
    tags = []
    for ex in data:
        tags.extend(ex.get("metadata", {}).get("tags", []))
    unique_tags = set(tags)
    
    print(f"\n--- {name} Analysis ---")
    print(f"Total Examples:   {len(data)}")
    print(f"Unique Questions: {len(unique_questions)} ({(len(unique_questions)/len(data))*100:.0f}% variance)")
    print(f"Unique Tags:      {len(unique_tags)} {list(unique_tags)[:5]}")
    
    # Check for critical dimensions
    has_edge_cases = any("edge-case" in t for t in tags)
    has_adversarial = any("adversarial" in t for t in tags)
    
    print(f"Includes Edge Cases:  {'✅ Yes' if has_edge_cases else '❌ No'}")
    print(f"Includes Adversarial: {'✅ Yes' if has_adversarial else '❌ No'}")

def main():
    print("=" * 60)
    print("Dataset Quality Comparison: Biased vs Golden")
    print("=" * 60)
    
    biased_path = DATA_DIR / "biased_dataset.json"
    golden_path = DATA_DIR / "golden_dataset.json"
    
    if not biased_path.exists() or not golden_path.exists():
        print("[ERROR] Ensure both biased_dataset.json and golden_dataset.json exist in data/")
        return
        
    analyze_dataset("Biased Dataset (Poor Engineering)", biased_path)
    analyze_dataset("Golden Dataset (Robust Engineering)", golden_path)
    
    print("\n" + "=" * 60)
    print("Conclusion: Evaluating against the biased dataset will yield artificially")
    print("high scores that collapse in production. The golden dataset enforces")
    print("coverage across factual, multi-part, and adversarial user inputs.")
    print("=" * 60)

if __name__ == "__main__":
    main()