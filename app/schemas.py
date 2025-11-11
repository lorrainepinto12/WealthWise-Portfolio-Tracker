from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum
from typing import List

#User Schemas 
class UserBase(BaseModel):
    name: str
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "email": "johndoe@gmail.com"
            }
        }
    }

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "johndoe@gmail.com"
            }
        }
    }

#Transaction Schemas
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

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "symbol": "TCS",
                "type": "BUY",
                "units": 5,
                "price": 3200,
                "date": "2025-05-10"
            }
        }
    }

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "symbol": "TCS",
                "type": "BUY",
                "units": 5,
                "price": 3200,
                "date": "2025-05-10"
            }
        }
    }

#Portfolio Summary Schema
class Holding(BaseModel):
    symbol: str
    units: float
    avg_cost: float
    current_price: float
    unrealized_pl: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "symbol": "TCS",
                "units": 5,
                "avg_cost": 3200,
                "current_price": 3400,
                "unrealized_pl": 1000
            }
        }
    }

class PortfolioSummary(BaseModel):
    user_id: int
    holdings: List[Holding]
    total_value: float
    total_gain: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "holdings": [
                    {
                        "symbol": "TCS",
                        "units": 5,
                        "avg_cost": 3200,
                        "current_price": 3400,
                        "unrealized_pl": 1000
                    }
                ],
                "total_value": 17000,
                "total_gain": 1000
            }
        }
    }
