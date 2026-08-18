# NexRoute Chatbot API

A FastAPI-based chatbot application starter project.

## Project structure

```text
NexRoute/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── deps.py
│   ├── core/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── __init__.py
│   ├── main.py
│   └── tests/
├── .gitignore
├── README.md
├── requirements.txt
└── .env.example
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Routes

- `GET /health`
- `POST /api/chat` for chatbot requests
## Features

- The project now has `Routing` strategy among the agents.
- At very first there is semantic model `BAAI/bge-small-en-v1.5` trained on two intents read and write.
- If the result by the classifier is `ambigious` in `intent: ambigious` then there is fallback mechanism where we use an llm to produce the intent feild.
- Later versions will log those ambigious statements so the model can be improved. 
- `Read and Write` agents have been configured but for now there is no tool attached to them.
## Configuration

Copy `.env.example` to `.env` and update the values as needed.
