import datetime

from sqlalchemy import Column, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core import Base
from app.schemas import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_id = Column(Integer, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    organization_name = Column(String, nullable=True)
    sign_in_code = Column(String, unique=True, nullable=True)
    created_at = DateTime(default=datetime.datetime.now())
    updated_at = DateTime(default=datetime.datetime.now(), nullable=True)