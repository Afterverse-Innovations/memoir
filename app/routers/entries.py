from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.database import get_db
from app.models.entry import Entry
from app.schemas.entry import EntryCreate, EntryResponse
router = APIRouter()


@router.post("/entries", response_model=EntryResponse)
async def create_entry(entry_data: EntryCreate, db: AsyncSession = Depends(get_db)):
    entry = Entry(
        content=entry_data.content,
        mood=entry_data.mood
    )

    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return entry


@router.get("/entries", response_model=list[EntryResponse])
async def get_entries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Entry)
        .where(Entry.deleted_at.is_(None))
        .order_by(Entry.created_at.desc())
    )
    return result.scalars().all()


@router.get("/entries/{entry_id}", response_model=EntryResponse)
async def get_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Entry)
        .where(Entry.id == entry_id, Entry.deleted_at.is_(None))
    )

    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    return entry


@router.delete("/entries/{entry_id}")
async def delete_entry(entry_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Entry)
        .where(Entry.id == entry_id, Entry.deleted_at.is_(None))
    )

    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    entry.deleted_at = datetime.utcnow()
    await db.commit()

    return {"message": "Entry deleted"}