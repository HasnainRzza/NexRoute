from fastapi import APIRouter, Query
from agents.read.read_agent import read_agent as ra
from agents.write.write_agent import write_agent as wa
from services.classifier import classify

router = APIRouter()


@router.post("/chat")
async def chat(query: str = Query(..., min_length=1, max_length=2000)):
    classification_result = await classify(query)

    if classification_result["intent"] == "read":
        response = await ra(query)
        return {"query": query, "response": response}

    if classification_result["intent"] == "write":
        response = await wa(query)
        return {
            "query": query,
            "response": {response}
        }

    return {"query": query, "response": "I couldn't confidently classify this request."}