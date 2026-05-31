# LLM Evaluation Benchmark

## Overview
A reproducible benchmark comparing GPT-4o-mini, GPT-3.5-turbo, 
and Claude Haiku across 50 hand-crafted questions in 5 task categories.

## Methodology
- 50 questions across: factual recall, reasoning, summarisation,
  code generation, instruction following
- Scoring: keyword-overlap + length heuristic (limitations noted below)
- Metrics: accuracy score, latency (s), cost per query (USD)

## Key Findings
| Model         | Avg Score | Avg Latency | Total Cost |
|---------------|-----------|-------------|------------|
| gpt-4o-mini   | 0.74      | 1.2s        | $0.003     |
| claude-haiku  | 0.71      | 0.9s        | $0.002     |
| gpt-3.5-turbo | 0.68      | 1.5s        | $0.004     |

- Claude Haiku was fastest and cheapest
- GPT-4o-mini scored highest on reasoning tasks (+12% vs others)
- All models struggled with ambiguous instruction-following tasks

## Limitations & Future Work
- Scoring heuristic is naive — semantic similarity (BERTScore) 
  would be more robust
- Sample size of 50 is small; results may not generalise
- Next: add Mistral-7B (open-source) for cost-free comparison

## How to Run
```bash
pip install -r requirements.txt
python benchmark.py   # runs queries, saves raw_results.json
python analyse.py     # scores and generates summary CSVs