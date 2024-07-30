from sqlalchemy.orm import Session
from schema.user import UserCreate
from models import user as user_model
import uuid

from service.auth import get_password_hash


def create_user(db: Session, user_create: UserCreate):
    # Create user
    user = user_model.User(
        id=uuid.uuid4(),
        email=user_create.email,
        password=get_password_hash(user_create.password),
        expired_date=user_create.expired_date
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    return user
