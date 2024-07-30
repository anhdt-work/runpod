from pydantic import BaseModel

from schema.token import Token


class ChatMessage(BaseModel):
    message: str
    token: Token
