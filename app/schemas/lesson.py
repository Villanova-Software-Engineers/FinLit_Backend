from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LessonBase(BaseModel):
    title: str
    content: str
    duration_minutes: int
    order_in_topic: int
    completion_rate: float = 0.0
    average_time_spent: float = 0.0
    quiz_aggregate_score: float = 0.0

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    duration_minutes: int | None = None
    order_in_topic: int| None = None

class LessonResponse(LessonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LessonAnalyticsBase(BaseModel):
    lesson_id: int
    completion_rate: float ### % of users who completed the lesson
    average_time_spent: float ### Average time spent on the lesson
    quiz_aggregate_score: float ### Average score across all quizzes in the lesson

class LessonAnalyticsResponse(LessonAnalyticsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LessonAnalyticsUpdate(BaseModel):
    completion_rate: float | None = None
    average_time_spent: float | None = None
    quiz_aggregate_score: float | None = None