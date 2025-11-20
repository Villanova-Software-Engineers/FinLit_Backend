from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    title = Column(String)
    total_questions = Column(Integer)
    questions = Column(JSONB)
    passing_score_percent = Column(Float)
    estimated_time_minutes = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    completion_rate = Column(Float)
    average_score = Column(Float)
    average_time_spent = Column(Float)
    average_attempts = Column(Float)
    drop_off_rate = Column(Float)

    lesson = relationship("Lesson", back_populates="quizzes")
