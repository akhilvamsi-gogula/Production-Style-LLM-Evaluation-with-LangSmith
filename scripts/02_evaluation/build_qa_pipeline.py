#!/usr/bin/env python3
"""Build a prompt-based Q&A pipeline for evaluation in LangSmith."""

import sys
from pathlib import Path
import re
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _env import load_project_env

load_project_env()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent.parent / "data"

def get_qa_pipeline(prompt_version="prompt_v1.txt", model_name="qwen/qwen3-32b"):
    """Factory function to build a QA pipeline with a specific prompt."""
    with open(DATA_DIR / prompt_version, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()

    llm = ChatGroq(model=model_name, temperature=0.1)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])
    chain = prompt | llm

    def qa_pipeline(inputs: dict) -> dict:
        time.sleep(4)  # SLEEP TO PREVENT GROQ 6000 TPM RATE LIMIT
        response = chain.invoke({"question": inputs["question"]})
        content = response.content
        
        # Strip <think> blocks common in Qwen/DeepSeek reasoning models
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        
        return {"output": content}
        
    return qa_pipeline, system_prompt

def main() -> None:
    print("=" * 60)
    print("Build Q&A Pipeline")
    print("=" * 60)

    qa_pipeline, system_prompt = get_qa_pipeline()
    print(f"\nLoaded system prompt:\n  {system_prompt[:80]}...")

    test_questions = [
        "What is the return policy for laptops?",
        "How much do CloudRunner Shoes cost?",
        "What is the meaning of life?",
    ]

    print("\nTesting pipeline:")
    for question in test_questions:
        result = qa_pipeline({"question": question})
        print(f"\n Q: {question}")
        print(f" A: {result['output'][:80]}...")

    print("\n" + "=" * 60)
    print("Q&A pipeline ready")
    print("=" * 60)

if __name__ == "__main__":
    main()