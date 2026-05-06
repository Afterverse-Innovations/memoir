from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class EntryCreate(BaseModel):
    content: str
    mood: str | None = None


class EntryResponse(BaseModel):
    id: UUID
    content: str
    mood: str | None
    created_at: datetime

    class Config:
        from_attributes = True 