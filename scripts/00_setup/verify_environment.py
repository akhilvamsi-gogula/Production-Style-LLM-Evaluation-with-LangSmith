#!/usr/bin/env python3
"""
Environment Verification
Checks Python packages, API connectivity, LangSmith connection, and data files.
"""

import os
import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Add ROOT_DIR to Python's import path
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from _env import load_project_env

load_project_env()

def check_pass(name):
    print(f" [PASS] {name}")
    return 1

def check_fail(name, detail=""):
    msg = f" [FAIL] {name}"
    if detail:
        msg += f" - {detail}"
    print(msg)
    return 0

def main():
    print("=" * 60)
    print("Production-Style LLM Evaluation - Environment Verification")
    print("=" * 60)

    results = []

    # 1. Check virtual environment
    print("\n[1/6] Virtual Environment")
    if hasattr(sys, 'prefix') and sys.prefix != sys.base_prefix:
        results.append(check_pass("Virtual environment is active"))
    else:
        results.append(check_fail("Virtual environment not active", "Activate your venv before running"))

    # 2. Check required packages
    print("\n[2/6] Required Packages")
    packages = {
        "langsmith": "langsmith",
        "langchain": "langchain",
        "langchain_groq": "langchain-groq",
        "groq": "groq",
        "dotenv": "python-dotenv"
    }
    for module, name in packages.items():
        try:
            __import__(module)
            results.append(check_pass(f"{name} installed"))
        except ImportError:
            results.append(check_fail(f"{name} not installed", f"Run: pip install {name}"))

    # 3. Check Groq API
    print("\n[3/6] Groq API Connection")
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        results.append(check_pass("GROQ_API_KEY is set"))
    else:
        results.append(check_fail("GROQ_API_KEY not set in .env"))

    # 4. Check LangSmith API key
    print("\n[4/6] LangSmith Configuration")
    langchain_key = os.environ.get("LANGCHAIN_API_KEY")
    tracing = os.environ.get("LANGCHAIN_TRACING_V2")
    project = os.environ.get("LANGCHAIN_PROJECT")

    if langchain_key:
        results.append(check_pass("LANGCHAIN_API_KEY is set"))
    else:
        results.append(check_fail("LANGCHAIN_API_KEY not set in .env"))

    if tracing == "true":
        results.append(check_pass("LANGCHAIN_TRACING_V2 is enabled"))
    else:
        results.append(check_fail("LANGCHAIN_TRACING_V2 not true in .env"))
        
    if project:
        results.append(check_pass(f"LANGCHAIN_PROJECT is set to: {project}"))
    else:
        results.append(check_fail("LANGCHAIN_PROJECT not set in .env"))

    # 5. Test LangSmith connection
    print("\n[5/6] LangSmith Connection")
    if langchain_key:
        try:
            from langsmith import Client
            client = Client()
            list(client.list_datasets(limit=1))
            results.append(check_pass("LangSmith API connected successfully"))
        except Exception as e:
            results.append(check_fail("LangSmith connection failed", str(e)[:80]))
    else:
        results.append(check_fail("LangSmith connection skipped", "Set LANGCHAIN_API_KEY first"))

    # 6. Check data files
    print("\n[6/6] Data Files")
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    data_files = {
        ROOT_DIR / "data" / "product_catalog.json": "Product Catalog",
        ROOT_DIR / "data" / "conversation_logs.json": "Conversation Logs",
        ROOT_DIR / "data" / "prompt_v1.txt": "Prompt V1",
        ROOT_DIR / "data" / "prompt_v2.txt": "Prompt V2"
    }
    for path, name in data_files.items():
        if path.exists():
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
    else:
        print(f"\n[ERROR] {total - passed} check(s) failed. Fix the issues before continuing.")

if __name__ == "__main__":
    main()