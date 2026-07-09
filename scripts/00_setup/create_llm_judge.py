#!/usr/bin/env python3
"""
Create an LLM-as-judge evaluator to score response helpfulness.
"""

import re
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from _env import load_project_env

load_project_env()

# Use a global variable but initialize it lazily inside the evaluator
_judge_llm = None

def get_judge_llm():
    global _judge_llm
    if _judge_llm is None:
        _judge_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    return _judge_llm

def llm_judge_evaluator(run, example) -> dict:
    # Safely handle if the run failed and returned None
    if not run.outputs or "output" not in run.outputs:
        return {"key": "helpfulness", "score": 0.0}
        
    question = example.inputs.get("question", "")
    response = run.outputs.get("output", "")
    reference = example.outputs.get("answer", "")
    
    judge_prompt = f"""Rate the helpfulness of this response on a scale of 1-5.

Question: {question}
Response: {response}
Reference Answer: {reference}

Scoring:
1 - Completely wrong or irrelevant
2 - Partially relevant but missing key information
3 - Correct but could be more helpful
4 - Good answer with relevant details
5 - Excellent, complete, and well-structured answer

Reply with ONLY a single number (1-5)."""

    llm = get_judge_llm()
    judge_response = llm.invoke([HumanMessage(content=judge_prompt)])
    try:
        score_text = judge_response.content.strip()
        score = int(re.search(r"[1-5]", score_text).group())
    except (ValueError, AttributeError):
        score = 3

    return {"key": "helpfulness", "score": score / 5.0}

def main() -> None:
    print("=" * 60)
    print("Create LLM-as-Judge Evaluator")
    print("=" * 60)

    class MockRun:
        def __init__(self, output):
            self.outputs = {"output": output}

    class MockExample:
        def __init__(self, question, answer):
            self.inputs = {"question": question}
            self.outputs = {"answer": answer}

    test_cases = [
        {
            "question": "What's your return policy?",
            "reference": "30-day return policy for unused items with receipt",
            "response": "30 days.",
            "label": "Minimal response",
        },
        {
            "question": "What's your return policy?",
            "reference": "30-day return policy for unused items with receipt",
            "response": "You can return unused items within 30 days with a receipt. Contact support for assistance.",
            "label": "Helpful response",
        },
        {
            "question": "What's your return policy?",
            "reference": "30-day return policy for unused items with receipt",
            "response": "I like pizza.",
            "label": "Irrelevant response",
        },
    ]

    for case in test_cases:
        run = MockRun(case["response"])
        example = MockExample(case["question"], case["reference"])
        result = llm_judge_evaluator(run, example)
        score_out_of_5 = result["score"] * 5
        print(f"\n [{case['label']}]")
        print(f"   Response:    {case['response']}")
        print(f"   Helpfulness: {score_out_of_5:.0f}/5")

    print("\n" + "=" * 60)
    print("LLM-as-judge evaluator ready")
    print("=" * 60)

if __name__ == "__main__":
    main()