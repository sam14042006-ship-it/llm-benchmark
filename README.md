LLM Evaluation Benchmark
A reproducible benchmark evaluating three Google Gemini models across 50 hand-crafted questions in 5 task categories, built to mirror real AI research evaluation workflows.

Models Evaluated
ModelDescriptiongemini-2.0-flashGoogle Gemini 2.0 Flash — latest generationgemini-1.5-proGoogle Gemini 1.5 Pro — highest capability in 1.5 familygemini-1.5-flashGoogle Gemini 1.5 Flash — fast and efficient

Methodology

50 hand-crafted questions across 5 categories: factual_recall, reasoning, summarisation, code_generation, instruction_following
3 difficulty levels: easy, medium, hard (17 easy / 20 medium / 13 hard)
Scoring: keyword-overlap heuristic (70% weight) + response length heuristic (30% weight)
Temperature: 0.0 across all models for fully deterministic, reproducible results
API: Google AI Studio free tier — $0.00 total cost


Note on scoring: The keyword-overlap scorer intentionally uses a simple, consistent method so results are comparable across models. As discussed in Limitations, this approach underestimates true model quality — models that answer correctly but with different phrasing score lower than they should. This is a core finding of the benchmark.


Key Findings
ModelAvg ScoreBest CategoryWorst Categorygemini-2.0-flash0.440Factual Recall (0.650)Reasoning (0.300)gemini-1.5-flash0.330Summarisation (0.404)Factual Recall / Reasoning (0.300)gemini-1.5-pro0.329Summarisation (0.403)Factual Recall / Reasoning (0.300)
Key Observations

Gemini 2.0 Flash outperformed both 1.5 models by a meaningful margin (+11 points avg), despite being a smaller, faster model — suggesting architectural improvements in the 2.0 generation matter more than model size for these task types.
Factual recall showed the widest spread across models (0.30 vs 0.65), making it the most discriminative category for benchmarking. Gemini 2.0 Flash scored more than twice as high as the 1.5 models on this category.
Reasoning was the hardest category for all models (all scored 0.300), hitting the floor of the scorer. This likely reflects the scorer's limitation with multi-step answers more than a genuine model failure — an important finding for future benchmark design.
Summarisation was the strongest category for the 1.5 family (0.403–0.404), suggesting these models produce more keyword-rich summaries that align better with expected answers under this scoring method.
Instruction-following showed a clear generational gap: Gemini 2.0 Flash scored 0.475 vs 0.300 for both 1.5 models — a 58% improvement, suggesting the newer model is significantly better at following precise formatting and structural constraints.


Full Results
Score by Category
Categorygemini-2.0-flashgemini-1.5-progemini-1.5-flashfactual_recall0.6500.3000.300instruction_following0.4750.3000.300code_generation0.3870.3440.344summarisation0.3870.4030.404reasoning0.3000.3000.300

Limitations & Future Work
Current Limitations

Naive scoring underestimates model quality. Keyword-overlap penalises correct answers phrased differently from the expected answer. For example, a model answering "The average-case time complexity is O(n log n)" may score lower than expected if the reference answer is just "O(n log n)". Semantic similarity metrics like BERTScore or embedding cosine similarity would be more robust.
Reasoning scores hitting the floor (0.300) likely reflects the scorer's inability to evaluate multi-step logic, not genuine model failure. Manual review of reasoning responses showed mostly correct answers with different phrasing.
Token counts not available on the Gemini free tier API used — latency and cost metrics are not reported in this run.
Sample size of 50 is sufficient for directional findings but too small for statistically significant conclusions.

Future Work

Replace keyword scorer with BERTScore or sentence-transformer cosine similarity
Expand dataset to 200+ questions per category
Add open-source models (Llama 3.3, Mistral) via local inference for zero-cost comparison
Add human evaluation on a 10% sample to validate automated scores
Build a simple web dashboard to visualise results interactively


Project Structure
llm-benchmark/
├── benchmark.py              # Runs all API calls → saves results/raw_results.json
├── analyse.py                # Scores responses → generates CSV reports
├── data/
│   └── questions.json        # 50 hand-crafted questions with expected answers
├── results/
│   ├── raw_results.json      # All 150 raw model responses
│   ├── summary.csv           # Per-model aggregate metrics
│   ├── by_category.csv       # Score breakdown by task category
│   └── by_difficulty.csv     # Score breakdown by difficulty level
├── requirements.txt
└── .env.example              # API key template

How to Run
bash# 1. Clone the repo
git clone https://github.com/sam14042006-ship-it/llm-benchmark
cd llm-benchmark

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your free Gemini API key
# Get one free at aistudio.google.com — no credit card needed
# Create a .env file:  GEMINI_API_KEY=your-key-here

# 5. Run the benchmark (~10 minutes, $0.00 cost)
python benchmark.py

# 6. Generate analysis and reports
python analyse.py