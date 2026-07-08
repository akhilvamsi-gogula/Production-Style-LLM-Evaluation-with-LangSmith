#!/usr/bin/env python3
"""
Environment Verification for Offline Evaluation Pipeline Lab
Checks Python packages, API connectivity, LangSmith connection, and data files.
"""

import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _env import load_project_env

load_project_env()


def check_pass(name):
    print(f"  [PASS] {name}")
    return True

def check_fail(name, detail=""):
    msg = f"  [FAIL] {name}"
    if detail:
        msg += f" - {detail}"
    print(msg)
    return False


def main():
    print("=" * 60)
    print("Offline Evaluation Pipeline - Environment Verification")
    print("=" * 60)

    results = []

    # 1. Check virtual environment
    print("\n[1/6] Virtual Environment")
    if hasattr(sys, 'prefix') and sys.prefix != sys.base_prefix:
        results.append(check_pass("Virtual environment is active"))
    else:
        results.append(check_fail("Virtual environment not active",
                                  "Run: source /root/venv/bin/activate"))

    # 2. Check required packages
    print("\n[2/6] Required Packages")
    packages = {
        "langsmith": "langsmith",
        "langchain": "langchain",
        "langchain_groq": "langchain-groq",
        "groq": "groq"
    }
    for module, name in packages.items():
        try:
            __import__(module)
            results.append(check_pass(f"{name} installed"))
        except ImportError:
            results.append(check_fail(f"{name} not installed",
                                      f"Run: pip install {name}"))

    # 3. Check Groq API
    print("\n[3/6] Groq API Connection")
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        results.append(check_pass("GROQ_API_KEY is set"))
    else:
        results.append(check_fail("GROQ_API_KEY not set"))

    # 4. Check LangSmith API key
    print("\n[4/6] LangSmith Configuration")
    langchain_key = os.environ.get("LANGCHAIN_API_KEY")
    tracing = os.environ.get("LANGCHAIN_TRACING_V2")

    if langchain_key:
        results.append(check_pass("LANGCHAIN_API_KEY is set"))
    else:
        results.append(check_fail("LANGCHAIN_API_KEY not set",
                                  'Run: export LANGCHAIN_API_KEY="your-key"'))

    if tracing == "true":
        results.append(check_pass("LANGCHAIN_TRACING_V2 is enabled"))
    else:
        results.append(check_fail("LANGCHAIN_TRACING_V2 not set",
                                  'Run: export LANGCHAIN_TRACING_V2=true'))

    # 5. Test LangSmith connection
    print("\n[5/6] LangSmith Connection")
    if langchain_key:
        try:
            from langsmith import Client
            client = Client()
            list(client.list_datasets(limit=1))
            results.append(check_pass("LangSmith API connected"))
        except Exception as e:
            results.append(check_fail("LangSmith connection", str(e)[:80]))
    else:
        results.append(check_fail("LangSmith connection",
                                  "Set LANGCHAIN_API_KEY first"))

    # 6. Check data files
    print("\n[6/6] Data Files")
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    data_files = {
        ROOT_DIR / "data" / "golden_dataset.json": "Golden dataset",
        ROOT_DIR / "data" / "prompt_v1.txt": "Prompt V1",
        ROOT_DIR / "data" / "prompt_v2.txt": "Prompt V2"
    }
    for path, name in data_files.items():
        if path.exists():
            if path.suffix == ".json":
                with open(path) as f:
                    data = json.load(f)
                results.append(check_pass(f"{name} ({len(data)} examples)"))
            else:
                results.append(check_pass(f"{name} found"))
        else:
            results.append(check_fail(f"{name} not found", str(path)))

    # Summary
    passed = sum(results)
    total = len(results)
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} checks passed")
    print("=" * 60)

    if passed == total:
        print("\n[OK] Environment verified! You are ready to start.")
        print("\nNext: Run scripts/00_setup/verify_environment.py and then the dataset and evaluation scripts")
    else:
        print(f"\n[ERROR] {total - passed} check(s) failed. Fix the issues above.")


if __name__ == "__main__":
    main()
