from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=50,
    messages=[
        {
            "role": "user",
            "content": "What is the average-case time complexity of merge sort?"
        }
    ]
)

print(response.content[0].text)