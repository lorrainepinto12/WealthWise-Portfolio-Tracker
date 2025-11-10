from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db  # Your database session dependency

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# ---------------- POST: Add a new transaction ----------------
@router.post("/", response_model=schemas.Transaction)
def add_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """
    Add a BUY or SELL transaction for a user.
    Validates that SELL transactions do not exceed holdings.
    """
    try:
        db_tx = crud.create_transaction(db, transaction)
        return db_tx
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------- GET: Get transactions for a user ----------------
@router.get("/{user_id}", response_model=list[schemas.Transaction])
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all transactions for a specific user.
    """
    transactions = crud.get_transactions_by_user(db, user_id)
    return transactions
