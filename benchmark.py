import json
from dotenv import load_dotenv
import os

load_dotenv()

print("OpenAI key found:", os.getenv("OPENAI_API_KEY") is not None)
print("Anthropic key found:", os.getenv("ANTHROPIC_API_KEY") is not None)

with open("data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions")

for q in questions:
    print(q["id"], "-", q["category"])

print("Success!")