from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db  

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/", response_model=schemas.Transaction , summary="Add a transaction" , description="Record a BUY or SELL transaction ")
def add_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """
    Add a BUY or SELL transaction for a user.
    Validates that SELL transactions do not exceed holdings.
    """
    try:
        return crud.create_transaction(db, transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=list[schemas.Transaction] , summary="Get user transactions", description="Fetch all transactions for a specific user")
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all transactions for a specific user.
    """
    transactions = crud.get_transactions_by_user(db, user_id)
    return transactions
