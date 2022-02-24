"""models user module."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    hash_password = Column(String, nullable=False)
    created_date: datetime = Column(DateTime, default=datetime.now, index=True)
    last_login: datetime = Column(DateTime, default=datetime.now, index=True)
    profile_image_url: str = Column(String)