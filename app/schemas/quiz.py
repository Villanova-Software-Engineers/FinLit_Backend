from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict, Any

class QuizBase(BaseModel):
    title: str
    total_questions: int
    questions: List[Dict[str, Any]]
    passing_score_percent: float
    estimated_time_minutes: int
    completion_rate: float = 0.0
    average_score: float = 0.0
    average_time_spent: float = 0.0
    average_attempts: float = 0.0
    drop_off_rate: float = 0.0

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
    quiz_id: int
    completion_rate: float ### % of users who completed the quiz
    average_score: float ### Average score of the quiz
    average_time_spent: float ### Average time spent on the quiz
    average_attempts: float ### Average number of attempts per user
    drop_off_rate: float ### % of users who started but did not complete the quiz
    
class QuizAnalyticsResponse(QuizAnalyticsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class QuizAnalyticsUpdate(BaseModel):
    completion_rate: float | None = None
    average_score: float | None = None
    average_time_spent: float | None = None
    average_attempts: float | None = None
    drop_off_rate: float | None = None