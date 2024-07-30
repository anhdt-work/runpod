from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schema.user import UserCreate
from service import user as user_service

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/create")
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    if user_service.get_user_by_email(db, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email already registered",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_service.create_user(db, user_create)
