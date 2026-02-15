from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import UserRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.FREE

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class CardBase(BaseModel):
    name: str
    purchase_price: float
    current_market_price: Optional[float] = None
    grade: Optional[str] = None
    status: str = "IN_INVENTORY"

class CardCreate(CardBase):
    pass

class CardUpdate(CardBase):
    pass

class CardResponse(CardBase):
    id: int
    owner_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class EmailSchema(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    attachment_path: Optional[str] = None

class TelegramSchema(BaseModel):
    message: str
