from fastapi import APIRouter, HTTPException
import requests
from fastapi.responses import StreamingResponse

from schema.chat import ChatMessage
from config.setting import MODEL_ENDPOINT
from langchain_community.llms import Ollama
ollama = Ollama(
    base_url=MODEL_ENDPOINT,
    model="deepseek-coder-v2"
)
router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/message")
def send_message(chat_message: ChatMessage) -> StreamingResponse:
    try:
        response = ollama.astream(chat_message.message)
        return StreamingResponse(response, media_type='text/event-stream')
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/message")
async def send_message():
    return 1
    try:
        response = ollama.astream("say 123")
        return StreamingResponse(response, media_type='text/event-stream')
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
