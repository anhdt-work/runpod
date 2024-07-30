from datetime import timedelta, datetime

from passlib.context import CryptContext
import jwt
from config.setting import TIME_ZONE
from models import user as user_model

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(password: str, user: user_model.User):
    if not verify_password(password, user.password):
        return False
    return True


def create_access_token(data: dict, user: user_model.User) -> str:
    to_encode = data.copy()
    expire = datetime.now(TIME_ZONE) + get_access_token_time_expired(user)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_access_token_time_expired(user: user_model.User) -> timedelta:
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
