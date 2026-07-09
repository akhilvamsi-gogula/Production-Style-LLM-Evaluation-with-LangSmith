# 🧪 Production-Style LLM Evaluation with LangSmith

[![LangSmith](https://img.shields.io/badge/LangSmith-Enabled-blue.svg)](https://smith.langchain.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20Llama%203.1-orange)](https://groq.com/)
[![Cost](https://img.shields.io/badge/Cost-Free%20Tier-brightgreen)](#)

A comprehensive, production-ready prototype demonstrating how to build, evaluate, and regression-test an LLM-powered customer support assistant using **LangSmith**.

While this specific use case is a straightforward e-commerce Q&A bot, the **evaluation architecture** is designed for enterprise scale. This project moves beyond simple "chatbots" and focuses on the rigorous Quality Engineering (QE) required to put LLMs into production safely.

## 🎯 The Core Problem & Solution

LLM systems often look great in demos but fail in edge cases, hallucinate, or become unhelpful when prompts are tweaked. **How do you know if a prompt change made your model better or worse?**

This repository solves this by implementing a **CI/CD-style evaluation pipeline** that:
1. Tests the LLM against a **Golden Dataset** (including edge cases and adversarial queries).
2. Uses **Keyword Coverage** to ensure factual accuracy (prices, policies, specs).
3. Uses an **LLM-as-a-Judge** to evaluate the tone, clarity, and helpfulness of the response.
4. Generates a **Go/No-Go Production Report** based on strict scoring thresholds.

---

## 🛠️ Architecture & Key Learnings

### 1. Dual-Evaluator System
To get a holistic view of LLM performance, this project uses two distinct evaluators running in parallel via LangSmith:
* **Deterministic (Keyword Evaluator):** A strict Python function checking if exact phrases from the Golden Dataset appear in the output.
* **Heuristic (LLM Judge):** Powered by Groq's `llama-3.1-8b-instant`, this evaluator grades the target model (Qwen 3) on a scale of 1-5 for helpfulness.

### 2. The Impact of Prompt Engineering (A Case Study)
During development, the pipeline highlighted how sensitive LLMs are to system prompts. 

* **Iteration 1:** When instructed to simply *"Answer the question in as few words as possible,"* the model failed the helpfulness threshold (scoring ~0.50). The LLM Judge recognized the answers were too robotic.
* **Iteration 2 (Context Injection):** The model failed factual checks because it didn't have access to the data. We implemented an injection step to pass the `product_catalog.json` directly into the system prompt context window.
* **Iteration 3 (The Final Prompt):** We updated the prompt to explicitly state: *"ALWAYS quote the exact phrases, numbers, and terminology from the product catalog. Do not rephrase."* 
* **The Result:** Keyword coverage jumped from 48% to over 60%, and Helpfulness climbed past 70%, passing the production thresholds!

### 3. Engineering for the Free Tier (Zero-Cost Architecture)
This entire pipeline was built and tested using **100% free-tier APIs**. When injecting large JSON context into prompts, we quickly hit Groq's 6,000 Tokens Per Minute (TPM) limit. To solve this, the pipeline includes:
* **Concurrency Control:** `max_concurrency=1` in LangSmith's `evaluate()` function to prevent API flooding.
* **Artificial Delays:** Implementing `time.sleep()` between evaluation loops to respect TPM windows.
* **Model Optimization:** Using the ultra-fast Llama 3.1 for the judging task to save token budget.
* **Regex Cleaning:** Using regex to strip `<think>` blocks from reasoning models before they reach the evaluators to preserve token counts and evaluator accuracy.

---

## 📸 Pipeline in Action

### 1. Environment Verification
Automated scripts verify that all API keys, dependencies, and datasets are present before launching the pipeline.
![Environment Setup](Results%20snapshots/env-setup.PNG)

### 2. Prompt Comparison in LangSmith
LangSmith UI comparing how different prompt versions alter the exact same dataset runs, allowing for easy regression testing.
![Prompt Comparison](Results%20snapshots/Langsmith%20different%20prompts%20comparision.PNG)

### 3. Real-Time Evaluation Scoring
The LangSmith dashboard showing the LLM Judge and Keyword Evaluator scoring the model's responses in real-time.
![Evaluation Results](Results%20snapshots/Langsmith%20result.PNG)

### 4. Automated Production Decision
The final script aggregating scores from LangSmith to make a Go/No-Go deployment decision based on predefined thresholds.
![Production Ready](Results%20snapshots/Green%20flag%20for%20production%20release.PNG)

---

## 🚀 Getting Started

### 1. Setup
Clone the repository, create a virtual environment, and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory:
```bash
LANGCHAIN_API_KEY="your_langsmith_key"
GROQ_API_KEY="your_groq_key"
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT="langsmith-evaluation-prototype"
```

### 3. Execution Order

**Phase 0: Environment Setup**
```bash
python scripts/00_setup/verify_environment.py
python scripts/00_setup/create_keyword_evaluator.py
python scripts/00_setup/create_llm_judge.py
```

**Phase 1: Dataset Creation & Management**
```bash
python scripts/01_dataset/build_dataset.py
python scripts/01_dataset/upload_dataset.py
python scripts/01_dataset/version_dataset.py
python scripts/01_dataset/tag_and_filter.py
```

**Phase 2: Evaluation Pipeline**
```bash
python scripts/02_evaluation/build_qa_pipeline.py
python scripts/02_evaluation/run_experiment.py
python scripts/02_evaluation/run_coverage_test.py
python scripts/02_evaluation/compare_experiments.py
```

**Phase 3: Automated Reporting**
```bash
python scripts/03_reporting/production_report.py
```

---

## 💼 Portfolio Positioning
This repository demonstrates a deep, practical understanding of **LLMOps**. It showcases the ability to move beyond basic API calls and engineer reliable, measurable, cost-effective, and safe AI systems ready for production deployment.