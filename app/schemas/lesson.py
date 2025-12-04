from pydantic import BaseModel, ConfigDict
from datetime import datetime

class LessonBase(BaseModel):
    title: str
    content: str
    duration_minutes: int
    order_in_topic: int

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