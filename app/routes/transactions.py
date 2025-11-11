from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db  

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)
#Add a transaction
@router.post("/", response_model=schemas.Transaction, summary="Add a transaction", description="Record a BUY or SELL transaction") 
def add_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """
    Add a BUY or SELL transaction for a user.
    Validates that:
      1. User exists
      2. SELL transactions do not exceed holdings
      3. Symbol is valid
      4. Transaction type is valid
    """
 
    # Check if user exists
    user = crud.get_user(db, user_id=transaction.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if symbol is valid using mock prices
    from app.crud import load_mock_prices  # reuse your function
    mock_prices = load_mock_prices()
    if transaction.symbol not in mock_prices:
        raise HTTPException(status_code=400, detail=f"Invalid symbol: {transaction.symbol}")
    
    # Validate transaction type
    if transaction.type not in ["BUY", "SELL"]:
        raise HTTPException(status_code=400, detail=f"Invalid transaction type: {transaction.type}. Must be 'BUY' or 'SELL'.")

    # Proceed with transaction creation
    try:
        return crud.create_transaction(db, transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#Get transaction by user_id
@router.get("/{user_id}", response_model=list[schemas.Transaction], summary="Get user transactions", description="Fetch all transactions for a specific user")
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all transactions for a specific user.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = crud.get_transactions_by_user(db, user_id)
    return transactions

# Get all transactions (for admin or debugging)
@router.get("/", response_model=list[schemas.Transaction], summary="Get all transactions", description="Fetch every transaction (admin/debugging use)")
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return transactions

