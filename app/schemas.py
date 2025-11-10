from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum
from typing import List

# ---------- User Schemas  ----------
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# ---------- Transaction Schemas ----------
class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class TransactionBase(BaseModel):
    user_id: int
    symbol: str
    type: TransactionType
    units: float
    price: float
    date: date

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True

# ---------- Portfolio Summary Schemas ----------
class Holding(BaseModel):
    symbol: str
    units: float
    avg_cost: float
    current_price: float
    unrealized_pl: float

class PortfolioSummary(BaseModel):
    user_id: int
    holdings: List[Holding]
    total_value: float
    total_gain: float