from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
