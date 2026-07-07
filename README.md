# LangSmith LLM Evaluation Prototype

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

- data/ - unified datasets and prompt files for the prototype
- build_dataset.py - create the golden dataset
- add_edge_cases.py - add edge cases and adversarial examples
- upload_dataset.py - upload the dataset to LangSmith
- tag_and_filter.py - tag and filter examples by category
- version_dataset.py - create a versioned dataset copy
- run_coverage_test.py - run evaluation and analyze coverage gaps
- build_qa_pipeline.py - build the Q&A pipeline
- create_keyword_evaluator.py - create a keyword-based evaluator
- create_llm_judge.py - create an LLM-as-judge evaluator
- run_experiment.py - run the full evaluation experiment
- compare_experiments.py - compare prompt versions
- production_report.py - generate a production-readiness report
- verify_environment.py - verify the setup

## Getting started

1. Clone the repository
2. Create and activate a Python virtual environment
3. Install dependencies with `pip install -r requirements.txt`
4. Set your environment variables for LangSmith and the LLM provider
5. Run the scripts in order

## Suggested order

1. Run the dataset scripts to build and upload the evaluation set
2. Run the pipeline and evaluator scripts
3. Compare experiments and generate the production report

## Use case

This prototype is designed around a customer-support-style Q&A assistant where answer quality, edge-case handling, and prompt reliability matter.

## Portfolio positioning

This repository is intended to be showcased as a hands-on prototype demonstrating practical LLM evaluation and QA thinking using LangSmith.
