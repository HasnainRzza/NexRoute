from fastapi import FastAPI
from api.routes import chat as chat_router
from api.routes import intent as intent_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to NexRoute!"}

app.include_router(chat_router.router, prefix="/api")
app.include_router(intent_router.router, prefix="/api")
