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

## Configuration

Copy `.env.example` to `.env` and update the values as needed.
