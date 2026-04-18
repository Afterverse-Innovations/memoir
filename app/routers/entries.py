from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime

from app.models.entry import EntryCreate, EntryResponse

router = APIRouter()

DB = {}  # in-memory store


@router.post("/entries", response_model=EntryResponse)
def create_entry(entry: EntryCreate):
    entry_id = uuid4()
    created_at = datetime.utcnow()

    data = {
        "id": entry_id,
        "content": entry.content,
        "mood": entry.mood,
        "created_at": created_at
    }

    DB[str(entry_id)] = data
    return data
