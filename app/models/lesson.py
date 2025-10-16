from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    title = Column(String)
    content = Column(Text)
    duration_minutes = Column(Integer)
    order_in_topic = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    topic = relationship("Topic", back_populates="lessons")
    quizzes = relationship("Quiz", back_populates="lessons")

    __table_args__ = (
        UniqueConstraint('topic_id', 'title', name='uix_topic_title'),
    )