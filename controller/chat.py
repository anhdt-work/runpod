from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
import requests
from database import get_db
from schema.chat import ChatMessage
from schema.token import Token
from schema.user import UserLogin
from service import user as user_service
from service import auth as auth_service
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
        raise HTTPException(status_code=500, detail=str(e))us
        g
