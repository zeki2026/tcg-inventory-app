from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.database import get_db
from app.models import Card, User, CardStatus
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/roi")
async def get_dashboard_roi(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Calculate Total Investment (Purchase Price of all cards)
    result = await db.execute(
        select(func.sum(Card.purchase_price)).where(Card.owner_id == current_user.id)
    )
    total_investment = result.scalars().first() or 0.0

    # Calculate Total Current Value (Market Price of all cards)
    result = await db.execute(
        select(func.sum(Card.current_market_price)).where(Card.owner_id == current_user.id)
    )
    current_portfolio_value = result.scalars().first() or 0.0

    roi_percentage = 0.0
    if total_investment > 0:
        roi_percentage = ((current_portfolio_value - total_investment) / total_investment) * 100

    return {
        "total_investment": total_investment,
        "current_portfolio_value": current_portfolio_value,
        "roi_percentage": round(roi_percentage, 2),
        "user_role": current_user.role
    }
