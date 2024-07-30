from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schema.token import Token
from schema.user import UserLogin
from service import user as user_service
from service import auth as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
def login_for_access_token(user_login: UserLogin, db: Session = Depends(get_db)) -> Token:
    user = user_service.get_user_by_email(db, user_login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth_service.authenticate_user(user_login.password, user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, user
    )
    return Token(access_token=access_token, token_type="bearer")
