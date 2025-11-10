from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Enum for transaction type
class TransactionType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    transactions = relationship("Transaction", back_populates="user")

# Transaction table
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    units = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="transactions")
