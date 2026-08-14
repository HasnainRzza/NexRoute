from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    user_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    user_id: str | None = None


@router.post("", response_model=ChatResponse)
async def chat_with_bot(payload: ChatMessage) -> ChatResponse:
    reply = (
        "Hello! I’m the NexRoute chatbot. "
        f"You said: {payload.message}"
    )
    return ChatResponse(reply=reply, user_id=payload.user_id)
