# Production Style LLM Evaluation with LangSmith


A practical prototype for evaluating an LLM-powered support assistant using LangSmith.

This project demonstrates a production-minded workflow for:
- tracing LLM behavior,
- building and versioning a golden dataset,
- testing prompt changes,
- running offline evaluations,
- and comparing results before deployment.

## Why this project matters

LLM systems can look strong in demos but still fail on real-world edge cases. This prototype focuses on the quality engineering side of LLM applications:

- observability with LangSmith tracing,
- dataset quality and coverage,
- prompt evaluation and regression testing,
- and decision-making based on measurable scores.

## What is included

### Golden dataset workflow
This part focuses on building a high-quality evaluation dataset for product support Q&A, including:
- structured dataset creation,
- edge cases and adversarial examples,
- tagging and filtering,
- versioning,
- and coverage analysis.

### Offline evaluation workflow
This part builds a practical evaluation pipeline with:
- a Q&A pipeline,
- keyword-based evaluators,
- an LLM-as-judge evaluator,
- multi-metric experiment runs,
- and a production-readiness report.

## Project structure

```
scripts/
├── 00_setup/
│   ├── verify_environment.py      # Verify environment setup
│   ├── create_keyword_evaluator.py # Create keyword-based evaluator
│   └── create_llm_judge.py        # Create LLM-as-judge evaluator
├── 01_dataset/
│   ├── build_dataset.py           # Create the golden dataset
│   ├── upload_dataset.py          # Upload dataset to LangSmith
│   ├── version_dataset.py         # Create versioned dataset copy
│   └── tag_and_filter.py          # Tag and filter examples by category
├── 02_evaluation/
│   ├── build_qa_pipeline.py       # Build the Q&A pipeline
│   ├── run_experiment.py          # Run full evaluation experiment
│   ├── run_coverage_test.py       # Run evaluation and analyze coverage gaps
│   └── compare_experiments.py     # Compare prompt versions
└── 03_reporting/
    └── production_report.py       # Generate production-readiness report

data/ - unified datasets and prompt files for the prototype
```

## Getting started

1. Clone the repository
2. Create and activate a Python virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Set your environment variables for LangSmith and the LLM provider (see `.env.example`)
5. Run the scripts in order (see Execution Order below)

## Execution Order

### Phase 0: Setup
```bash
python scripts/00_setup/verify_environment.py
python scripts/00_setup/create_keyword_evaluator.py
python scripts/00_setup/create_llm_judge.py
```

### Phase 1: Dataset Creation & Management
```bash
python scripts/01_dataset/build_dataset.py
python scripts/01_dataset/upload_dataset.py
python scripts/01_dataset/version_dataset.py
python scripts/01_dataset/tag_and_filter.py
```

### Phase 2: Evaluation Pipeline
```bash
python scripts/02_evaluation/build_qa_pipeline.py
python scripts/02_evaluation/run_experiment.py
python scripts/02_evaluation/run_coverage_test.py
python scripts/02_evaluation/compare_experiments.py
```

### Phase 3: Reporting
```bash
python scripts/03_reporting/production_report.py
```

## Use case

## Use case

This prototype is designed around a customer-support-style Q&A assistant where answer quality, edge-case handling, and prompt reliability matter.

## Portfolio positioning

This repository is intended to be showcased as a hands-on prototype demonstrating practical LLM evaluation and QA thinking using LangSmith.
