from openai import OpenAI
from dotenv import load_dotenv
import os

MAX_HISTORY = 2
MAX_OUTPUT_TOKEN = 80

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
)

MODEL = os.getenv("OPENROUTER_MODEL")

messages = [
    {"role": "system", "content": "Jawab Singkat, Jelas Maksimal 3-5 kalimat kecuali emang benar di minta detail"}
]

def trims_history():
    global messages
    messages = [messages[0]] + messages[-MAX_HISTORY:]

def ask_ai(prompt):
    messages.append({"role": "user", "content": prompt})
    
    raw  = client.chat.completions.with_raw_response.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_OUTPUT_TOKEN
    )

    response = raw.parse()
    headers = raw.headers

    limit = headers.get("x-ratelimit-limit-requests")
    remaining = headers.get("x-ratelimit-remaining-requests")
    reset = headers.get("x-ratelimit-reset-requests")

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return reply, limit, remaining, reset
