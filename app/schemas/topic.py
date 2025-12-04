from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TopicBase(BaseModel):
    name: str
    description: str
    attempts: int = 0
    completed: int = 0
    total_time_spent: float = 0.0
    total_score: float = 0.0

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TopicAnalyticsBase(BaseModel):
    completion_rate: float ### % of users who completed the topic
    average_time_spent: float ### Average time spent on the topic
    average_score: float ### Average score across all quizzes in the topic
    drop_off_rate: float ### % of users who started but did not complete the topic

class TopicAnalyticsUpdate(BaseModel):
    attempts: int | None = None
    completed: int | None = None
    total_time_spent: float | None = None
    total_score: float | None = None

class TopicAnalyticsResponse(TopicAnalyticsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

