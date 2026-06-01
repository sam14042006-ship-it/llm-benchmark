import time
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# All 3 models are FREE on Google AI Studio
MODELS = {
    "gemini-1.5-flash": {
        "model_id":    "gemini-1.5-flash",
        "description": "Google Gemini 1.5 Flash — fast and efficient"
    },
    "gemini-1.5-pro": {
        "model_id":    "gemini-1.5-pro",
        "description": "Google Gemini 1.5 Pro — most capable free model"
    },
    "gemini-2.0-flash": {
        "model_id":    "gemini-2.0-flash",
        "description": "Google Gemini 2.0 Flash — latest generation"
    },
}


def query_model(model_name, prompt):
    cfg = MODELS[model_name]
    model = genai.GenerativeModel(
        model_name=cfg["model_id"],
        system_instruction="You are a helpful assistant. Answer concisely and accurately."
    )

    start = time.time()
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.0,
            max_output_tokens=300,
        )
    )
    latency = round(time.time() - start, 3)
    text = response.text

    # Gemini free tier doesn't expose token counts in same way, estimate:
    tokens_in  = len(prompt.split()) * 1.3
    tokens_out = len(text.split()) * 1.3

    return {
        "response":   text,
        "latency_s":  latency,
        "tokens_in":  int(tokens_in),
        "tokens_out": int(tokens_out),
        "cost_usd":   0.0  # Free tier
    }


def run_benchmark(questions_path="data/questions.json"):
    with open(questions_path) as f:
        questions = json.load(f)

    results   = []
    total     = len(questions) * len(MODELS)
    completed = 0

    print("=" * 60)
    print("  LLM BENCHMARK — Google Gemini (Free Tier)")
    print("=" * 60)
    print(f"Questions : {len(questions)}")
    print(f"Models    : {', '.join(MODELS.keys())}")
    print(f"Total     : {total} API calls")
    print(f"Cost      : $0.00 (Google AI Studio free tier)")
    print("=" * 60 + "\n")

    for q in questions:
        for model_name in MODELS:
            completed += 1
            print(f"[{completed:>3}/{total}] {model_name:<22} | {q['id']}", end=" ... ", flush=True)

            try:
                result = query_model(model_name, q["question"])
                results.append({
                    "question_id": q["id"],
                    "category":    q["category"],
                    "difficulty":  q["difficulty"],
                    "question":    q["question"],
                    "model":       model_name,
                    **result
                })
                print(f"✓  ({result['latency_s']}s)")

            except Exception as e:
                print(f"✗  ERROR: {e}")
                results.append({
                    "question_id": q["id"],
                    "category":    q["category"],
                    "difficulty":  q["difficulty"],
                    "question":    q["question"],
                    "model":       model_name,
                    "response":    f"ERROR: {e}",
                    "latency_s":   0,
                    "tokens_in":   0,
                    "tokens_out":  0,
                    "cost_usd":    0
                })

            # Small delay to respect free tier rate limits
            time.sleep(1.0)

    os.makedirs("results", exist_ok=True)
    out_path = "results/raw_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    success = sum(1 for r in results if not r["response"].startswith("ERROR"))
    print(f"\n{'='*60}")
    print(f"Benchmark complete!")
    print(f"Successful calls : {success}/{total}")
    print(f"Results saved to : {out_path}")
    print(f"Total cost       : $0.00")
    print(f"{'='*60}")
    print(f"\nNext step: run  python analyse.py")


if __name__ == "__main__":
    run_benchmark()
