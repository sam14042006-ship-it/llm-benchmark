from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

print("OpenAI key found:", openai_key is not None)
print("Anthropic key found:", anthropic_key is not None)