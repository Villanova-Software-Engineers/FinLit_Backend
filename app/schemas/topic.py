from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TopicBase(BaseModel):
    name: str
    description: str
    completion_rate: float = 0.0
    average_time_spent: float = 0.0
    average_score: float = 0.0

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
    topic_id: int
    completion_rate: float ### % of users who completed the topic
    average_time_spent: float ### Average time spent on the topic
    average_score: float ### Average score across all quizzes in the topic

class TopicAnalyticsResponse(TopicAnalyticsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TopicAnalyticsUpdate(BaseModel):
    completion_rate: float | None = None
    average_time_spent: float | None = None
    average_score: float | None = None