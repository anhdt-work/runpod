from fastapi import APIRouter, HTTPException
import requests
from schema.chat import ChatMessage

from config.setting import MODEL_ENDPOINT

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/message")
def send_message(chat_message: ChatMessage) -> str:
    try:
        response = requests.post(MODEL_ENDPOINT, json=chat_message.dict())
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
