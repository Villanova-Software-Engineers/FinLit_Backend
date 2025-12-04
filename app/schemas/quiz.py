from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict, Any

class QuizBase(BaseModel):
    title: str
    total_questions: int
    questions: List[Dict[str, Any]]
    passing_score_percent: float
    estimated_time_minutes: int
    attempts: int = 0
    completed: int = 0
    total_score: float = 0.0
    total_time_spent: float = 0.0

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

class QuizAnalyticsBase(BaseModel):
    completion_rate: float ### % of users who completed the quiz
    average_score: float ### Average score of the quiz
    average_time_spent: float ### Average time spent on the quiz
    drop_off_rate: float ### % of users who started but did not complete the quiz

class QuizAnalyticsUpdate(BaseModel):
    attempts: int | None = None
    completed: int | None = None
    total_score: float | None = None
    total_time_spent: float | None = None
    
class QuizAnalyticsResponse(QuizAnalyticsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
