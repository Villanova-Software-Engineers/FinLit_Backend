from pydantic import BaseModel
from datetime import datetime

class TopicBase(BaseModel):
    name: str
    description: str

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True