import datetime

from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    expired_date: datetime.date
    confirm_password: str


class UserCreate(User):
    confirm_password: str
