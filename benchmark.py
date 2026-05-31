from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

question = "What is the average-case time complexity of merge sort?"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ]
)

print(response.choices[0].message.content)