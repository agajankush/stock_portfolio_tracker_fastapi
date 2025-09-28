# schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

# ============ Token Schemas ============

class Token(BaseModel):
    access_token: str
    token_type: str

# ============ User Schemas ============

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(...,min_length=8, max_length=64)

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# ============ Transaction Schemas ============

class TransactionCreate(BaseModel):
    ticker_symbol: str
    quantity: float
    price: float
    type: str # "BUY" or "SELL"

# ============ Portfolio Schemas ============

class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    user_id: int
    # transactions: List[Transaction] = [] # We will add this later

    class Config:
        from_attributes = True