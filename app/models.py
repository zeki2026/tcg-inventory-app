import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class UserRole(str, enum.Enum):
    FREE = "free"
    PRO = "pro"

class CardStatus(str, enum.Enum):
    IN_INVENTORY = "IN_INVENTORY"
    FOR_SALE = "FOR_SALE"
    SOLD = "SOLD"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.FREE)
    created_at = Column(DateTime, default=datetime.utcnow)

    cards = relationship("Card", back_populates="owner")

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_market_price = Column(Float, nullable=True)
    grade = Column(String, nullable=True) # e.g. PSA 10
    status = Column(Enum(CardStatus), default=CardStatus.IN_INVENTORY)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="cards")
