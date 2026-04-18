from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from uuid import UUID


class Mood(str, Enum):
    happy = "happy"
    neutral = "neutral"
    sad = "sad"
    anxious = "anxious"
    grateful = "grateful"


class EntryCreate(BaseModel):
    content: str
    mood: Mood | None = None


class EntryResponse(BaseModel):
    id: UUID
    content: str
    mood: Mood | None
    created_at: datetime
    