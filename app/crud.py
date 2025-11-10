from sqlalchemy.orm import Session
from app import models, schemas
import json
from pathlib import Path
# ---------- User CRUD ----------
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# ---------- Transaction CRUD ----------
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    # Validate SELL: cannot sell more units than owned
    if transaction.type == "SELL":
        txs = db.query(models.Transaction)\
                 .filter(models.Transaction.user_id == transaction.user_id,
                         models.Transaction.symbol == transaction.symbol).all()
        bought = sum(t.units for t in txs if t.type == "BUY")
        sold = sum(t.units for t in txs if t.type == "SELL")
        if transaction.units > (bought - sold):
            raise ValueError("Cannot sell more units than owned")
    
    db_tx = models.Transaction(**transaction.model_dump())
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

def get_transactions_by_user(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()

# ---------- Portfolio Summary CRUD ----------
MOCK_PRICES_FILE = Path("data/mock_prices.json")

def load_mock_prices():
    with open(MOCK_PRICES_FILE, "r") as f:
        return json.load(f)

def get_portfolio_summary(db: Session, user_id: int) -> schemas.PortfolioSummary:
    transactions = get_transactions_by_user(db, user_id)
    mock_prices = load_mock_prices()

    holdings_dict = {}  # symbol -> {units, total_cost}

    for tx in transactions:
        if tx.symbol not in holdings_dict:
            holdings_dict[tx.symbol] = {"units": 0, "total_cost": 0.0}

        if tx.type == "BUY":
            holdings_dict[tx.symbol]["total_cost"] += tx.units * tx.price
            holdings_dict[tx.symbol]["units"] += tx.units
        elif tx.type == "SELL":
            avg_cost = (holdings_dict[tx.symbol]["total_cost"] / holdings_dict[tx.symbol]["units"])
            holdings_dict[tx.symbol]["total_cost"] -= avg_cost * tx.units
            holdings_dict[tx.symbol]["units"] -= tx.units

    holdings_list = []
    total_value = 0.0
    total_gain = 0.0

    for symbol, data in holdings_dict.items():
        if data["units"] <= 0:
            continue  # Skip symbols with zero units

        current_price = mock_prices.get(symbol, 0)
        avg_cost = data["total_cost"] / data["units"]
        unrealized_pl = (current_price - avg_cost) * data["units"]

        holdings_list.append(schemas.Holding(
            symbol=symbol,
            units=data["units"],
            avg_cost=avg_cost,
            current_price=current_price,
            unrealized_pl=unrealized_pl
        ))

        total_value += current_price * data["units"]
        total_gain += unrealized_pl

    return schemas.PortfolioSummary(
        user_id=user_id,
        holdings=holdings_list,
        total_value=total_value,
        total_gain=total_gain
    )