# LLM-SafeMit: Evaluating and Verifying LLM-Assisted Mitigation Decisions in SDN

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper Status](https://img.shields.io/badge/Paper-Under%20Review-lightgrey)](#)

This repository contains the official implementation and evaluation data for the paper **"Evaluating and Verifying LLM-Assisted Mitigation Decisions in Software-Defined Networks"**.

## 📖 Overview

Large Language Models (LLMs) show promise in assisting network operators with security decisions in Software-Defined Networking (SDN). However, their free-form outputs are often unreliable for direct operational use due to parsing errors, policy violations, or vague targeting.

**LLM-SafeMit** proposes a controlled decision pipeline that combines:
1.  **Constrained Prompting:** Enforcing structured JSON outputs with predefined action/scope spaces.
2.  **Lightweight Validation:** A post-generation verification layer to ensure target specificity and policy compliance.

Our experiments on 30 SDN security scenarios using **Qwen2.5-1.5B** demonstrate that while unconstrained prompting yields only **63.33%** operationally good decisions, our proposed pipeline achieves **100%** reliability within the tested set.

## 📊 Key Results

The table below summarizes the operational reliability across three settings:

| Metric | Unconstrained | Constrained | Constrained + Validator |
| :--- | :---: | :---: | :---: |
| **Parse Success** | 76.67% | 100.00% | 100.00% |
| **Valid Action** | 86.67% | 100.00% | 100.00% |
| **Valid Scope** | 86.67% | 100.00% | 100.00% |
| **Specific Target** | 100.00% | 93.33% | 100.00% |
| **Policy Compliant** | 70.00% | 100.00% | 100.00% |
| **Operationally Good** | **63.33%** | **93.33%** | **100.00%** |

![Operational Reliability](figures/operationally_good_three_way_qwen2_5_1_5b.png)
*Figure: Improvement in operational reliability through constrained prompting and validation.*

## 📂 Repository Structure

├── data/
│   ├── scenarios_30.csv          # The 30 SDN security scenarios used for evaluation
│   └── ground_truth.csv          # Expected operational profiles for each scenario
├── src/
│   ├── prompts.py                # Logic for generating constrained vs. unconstrained prompts
│   ├── validator.py              # Implementation of the lightweight target-specificity validator
│   └── evaluate.py               # Main script to run evaluation metrics
├── results/
│   ├── raw_outputs/              # Raw LLM responses (JSON/Text)
│   ├── evaluated_results.csv     # Parsed and evaluated decisions
│   └── final_metrics.csv         # Aggregated metrics for the paper
├── figures/                      # Generated plots for the manuscript
├── notebooks/                    # Jupyter/Colab notebooks for step-by-step reproduction
├── requirements.txt              # Python dependencies
└── README.md
