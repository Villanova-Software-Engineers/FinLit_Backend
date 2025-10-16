from pydantic import BaseModel
from datetime import datetime
from typing import Any

class QuizBase(BaseModel):
    title: str
    passing_score_percent: float
    questions: Any

class QuizCreate(QuizBase):
    pass

class QuizUpdate(BaseModel):
    title: str | None = None
    passing_score_percent: float | None = None
    questions: Any | None = None

class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True