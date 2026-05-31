import json
import pandas as pd
from tabulate import tabulate

def simple_score(response: str, expected: str) -> float:
    """Naive scorer: keyword overlap + length penalty."""
    resp_lower = response.lower()
    exp_lower  = expected.lower()
    keywords   = exp_lower.split()
    
    hits = sum(1 for kw in keywords if kw in resp_lower)
    keyword_score = hits / len(keywords) if keywords else 0
    
    # penalise very long or very short responses
    ideal_len = len(expected) * 3
    len_ratio = min(len(response), ideal_len) / ideal_len
    
    return round((keyword_score * 0.7 + len_ratio * 0.3), 3)

def analyse(results_path="results/raw_results.json",
            questions_path="data/questions.json"):
    
    with open(results_path)  as f: results   = json.load(f)
    with open(questions_path) as f: questions = json.load(f)
    
    q_map = {q["id"]: q for q in questions}
    
    for r in results:
        q = q_map[r["question_id"]]
        r["score"] = simple_score(r["response"], q["expected_answer"])
    
    df = pd.DataFrame(results)
    
    summary = df.groupby("model").agg(
        avg_score   =("score",      "mean"),
        avg_latency =("latency_s",  "mean"),
        total_cost  =("cost_usd",   "sum"),
        avg_tokens  =("tokens_out", "mean")
    ).round(4)
    
    by_category = df.groupby(["model","category"])["score"].mean().unstack().round(3)
    
    print("\n=== OVERALL RESULTS ===")
    print(tabulate(summary, headers="keys", tablefmt="rounded_outline"))
    print("\n=== SCORE BY CATEGORY ===")
    print(tabulate(by_category, headers="keys", tablefmt="rounded_outline"))
    
    summary.to_csv("results/summary.csv")
    by_category.to_csv("results/by_category.csv")
    df.to_csv("results/full_results.csv", index=False)
    print("\nCSVs saved to results/")

if __name__ == "__main__":
    analyse()