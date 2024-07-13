import os
import openai
from config import apikey

openai.api_key = apikey

response = openai.chat.completions.create(
    messages=[{"role": "user", "content": "Write an email to my boss for resignation"}],
    model="gpt-4o",
)

print(response)
