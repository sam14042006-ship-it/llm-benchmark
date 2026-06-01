# LLM Evaluation Benchmark

A reproducible benchmark evaluating three Google Gemini models across **50 hand-crafted questions** in **5 task categories**, built to mirror real AI research evaluation workflows.

---

## Models Evaluated

| Model | Description |
|---|---|
| `gemini-2.0-flash` | Google Gemini 2.0 Flash — latest generation |
| `gemini-1.5-pro` | Google Gemini 1.5 Pro — highest capability in 1.5 family |
| `gemini-1.5-flash` | Google Gemini 1.5 Flash — fast and efficient |

---

## Methodology

- **50 hand-crafted questions** across 5 categories: `factual_recall`, `reasoning`, `summarisation`, `code_generation`, `instruction_following`
- **3 difficulty levels**: easy, medium, hard
- **Scoring**: keyword-overlap heuristic (70%) + response length heuristic (30%)
- **Temperature**: 0.0 across all models for fully deterministic results
- **API**: Google AI Studio free tier — $0.00 total cost

---

## Key Findings

| Model | Avg Score | Best Category | Worst Category |
|---|---|---|---|
| `gemini-2.0-flash` | **0.440** | Factual Recall (0.650) | Reasoning (0.300) |
| `gemini-1.5-flash` | 0.330 | Summarisation (0.404) | Factual Recall / Reasoning (0.300) |
| `gemini-1.5-pro` | 0.329 | Summarisation (0.403) | Factual Recall / Reasoning (0.300) |

### Key Observations

- **Gemini 2.0 Flash outperformed both 1.5 models** by 11 points on average
- **Factual recall showed the widest spread** — Gemini 2.0 Flash scored 2x higher than 1.5 models (0.65 vs 0.30)
- **Reasoning was hardest for all models** (all 0.300) — likely reflects scorer limitations with multi-step answers, not genuine model failure
- **Instruction-following showed the clearest generational gap**: 2.0 Flash scored 0.475 vs 0.300 for both 1.5 models (+58%)

---

## Score by Category

| Category | gemini-2.0-flash | gemini-1.5-pro | gemini-1.5-flash |
|---|---|---|---|
| factual_recall | **0.650** | 0.300 | 0.300 |
| instruction_following | **0.475** | 0.300 | 0.300 |
| code_generation | **0.387** | 0.344 | 0.344 |
| summarisation | 0.387 | **0.403** | **0.404** |
| reasoning | 0.300 | 0.300 | 0.300 |

---

## Limitations & Future Work

- **Naive scoring underestimates model quality** — keyword-overlap penalises correct answers phrased differently. BERTScore or embedding cosine similarity would be more robust
- **Reasoning floor at 0.300** likely reflects scorer inability to evaluate multi-step logic, not model failure — manual review confirmed mostly correct answers
- **Token counts unavailable** on Gemini free tier — latency and cost not reported
- Future: expand to 200+ questions, add open-source models (Llama 3, Mistral), build results dashboard

---

## Project Structure

llm-benchmark/
├── benchmark.py          # Runs all API calls → saves raw_results.json
├── analyse.py            # Scores responses → generates CSV reports
├── data/
│   └── questions.json    # 50 hand-crafted questions with expected answers
├── results/
│   ├── raw_results.json  # All 150 raw model responses
│   ├── summary.csv       # Per-model aggregate metrics
│   ├── by_category.csv   # Score breakdown by task category
│   └── by_difficulty.csv # Score breakdown by difficulty
├── requirements.txt
└── .env.example
---

## How to Run

```bash
git clone https://github.com/sam14042006-ship-it/llm-benchmark
cd llm-benchmark
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Add GEMINI_API_KEY to .env (free at aistudio.google.com)
python benchmark.py
python analyse.py
```

---
