from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from app.core import Base

class UserQuiz(Base):
    __tablename__ = "user_quiz"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), primary_key=True)
    score = Column(Float, nullable=True)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())