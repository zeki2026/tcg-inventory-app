from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.models import Card, User
from app.schemas import CardCreate, CardResponse, CardUpdate
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=CardResponse)
async def create_card(
    card: CardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_card = Card(**card.model_dump(), owner_id=current_user.id)
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card

@router.get("/", response_model=List[CardResponse])
async def read_cards(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Card).where(Card.owner_id == current_user.id).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get("/{card_id}", response_model=CardResponse)
async def read_card(
    card_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Card).where(Card.id == card_id, Card.owner_id == current_user.id)
    )
    card = result.scalars().first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: int,
    card_update: CardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Card).where(Card.id == card_id, Card.owner_id == current_user.id)
    )
    card = result.scalars().first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    
    for key, value in card_update.model_dump().items():
        setattr(card, key, value)
    
    await db.commit()
    await db.refresh(card)
    return card

@router.delete("/{card_id}")
async def delete_card(
    card_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Card).where(Card.id == card_id, Card.owner_id == current_user.id)
    )
    card = result.scalars().first()
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    
    await db.delete(card)
    await db.commit()
    return {"ok": True}
