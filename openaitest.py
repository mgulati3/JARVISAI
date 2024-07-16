import os
import openai
from config import apikey

openai.api_key = apikey

text = f"Openai response for prompt: Write an email to my boss for resignation \n *********************** \n\n"


response = openai.chat.completions.create(
    messages=[{"role": "user", "content": "Write an email to my boss for resignation"}],
    model="gpt-4o",
)

text += response.choices[0].message.content

print(text)

