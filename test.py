from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

#print("DEBUG KEY:", api_key)  # 👈 TEMP DEBUG

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Say hello"}],
)

print(response.choices[0].message.content)