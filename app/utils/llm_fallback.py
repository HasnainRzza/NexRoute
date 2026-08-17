from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")
client = Groq(
    api_key = GROQ_API_KEY
)

def fallback_classifier(query: str):
    completion = client.chat.completions.create(
        model= GROQ_MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": (f"You are the best classifier in the world. User will send you message you will have to tell weather user wants to do read task or write task. CRITICAL You should always answer in one word from [read, write]. USER MESSAGE: {query}")
            }
        ],
        temperature=0,
        top_p=0,
        stream=False,
        stop=None
    )

    return completion.choices[0].message.content

