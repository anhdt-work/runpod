from datetime import datetime

from sqlalchemy import Column, UUID, String, DateTime, Date
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.now())
    expired_date = Column(Date, nullable=False)
