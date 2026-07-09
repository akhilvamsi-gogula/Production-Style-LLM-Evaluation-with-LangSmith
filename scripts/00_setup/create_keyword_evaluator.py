#!/usr/bin/env python3
"""
Create a deterministic keyword-coverage evaluator for factual QA responses.
"""

def keyword_evaluator(run, example) -> dict:
    if not run.outputs or "output" not in run.outputs:
        return {"key": "keyword_coverage", "score": 0.0}
        
    prediction = run.outputs.get("output", "").lower()
    reference = example.outputs.get("answer", "").lower()

    keywords = reference.split()
    matches = sum(1 for keyword in keywords if keyword in prediction)
    score = matches / len(keywords) if keywords else 0.0

    return {"key": "keyword_coverage", "score": round(score, 2)}

def main() -> None:
    print("=" * 60)
    print("Create Keyword Evaluator")
    print("=" * 60)

    class MockRun:
        def __init__(self, output):
            self.outputs = {"output": output}

    class MockExample:
        def __init__(self, answer):
            self.outputs = {"answer": answer}

    test_cases = [
        {
            "reference": "30-day return policy for unused items with receipt",
            "response": "You can return items within 30 days if unused and you have a receipt",
            "label": "Rephrased response",
        },
        {
            "reference": "2-year manufacturer warranty",
            "response": "The warranty is 2 years from the manufacturer",
            "label": "Reworded response",
        },
        {
            "reference": "$149.99",
            "response": "They cost $149.99",
            "label": "Exact price",
        },
        {
            "reference": "Water resistant to 50 meters",
            "response": "I'm not sure about the water resistance.",
            "label": "Poor response",
        },
    ]

    for case in test_cases:
        run = MockRun(case["response"])
        example = MockExample(case["reference"])
        result = keyword_evaluator(run, example)
        print(f"\n [{case['label']}]")
        print(f"   Reference: {case['reference']}")
        print(f"   Response:  {case['response']}")
        print(f"   Coverage:  {result['score']:.2f}")

    print("\n" + "=" * 60)
    print("Keyword evaluator ready")
    print("=" * 60)

if __name__ == "__main__":
    main()