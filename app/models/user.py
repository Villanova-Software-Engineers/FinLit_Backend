from sqlalchemy import Column, String, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core import Base
from app.schemas import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    organization_name = Column(String, nullable=True)
    sign_in_code = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    quizzes = relationship("Quiz", secondary="user_quiz", back_populates="users")