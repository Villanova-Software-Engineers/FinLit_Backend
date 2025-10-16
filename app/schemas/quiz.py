from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict, Any

class QuizBase(BaseModel):
    title: str
    total_questions: int
    questions: List[Dict[str, Any]]
    passing_score_percent: float
    estimated_time_minutes: int

class QuizCreate(QuizBase):
    pass

class QuizUpdate(BaseModel):
    title: str | None = None
    total_questions: int | None = None
    questions: List[Dict[str, Any]] | None = None
    passing_score_percent: float | None = None
    estimated_time_minutes: int | None = None

class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)