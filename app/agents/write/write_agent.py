import os
from pathlib import Path

from dotenv import load_dotenv
from groq import AsyncGroq

BASE_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME")


async def write_agent(query: str):
    if not GROQ_API_KEY:
        return "Groq API key is not configured. Please set GROQ_API_KEY in the environment."

    client = AsyncGroq(api_key=GROQ_API_KEY)

    completion = await client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI Assistant working for NexRoute Organization. "
                    "Your task is to understand the user query and pick the best possible tool to get the required data. "
                    "For now you do not have any write tools, so reply that there is currently no write tool configured."
                ),
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        temperature=0,
        top_p=0,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content

