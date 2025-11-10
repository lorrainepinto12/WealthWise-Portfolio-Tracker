from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

@router.get("/summary", response_model=schemas.PortfolioSummary, summary="Get portfolio summary", description="Fetch holdings, total value, and gains for a user")
def get_portfolio_summary(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = crud.get_user_by_email(db, email=None) 
    try:
        summary = crud.get_portfolio_summary(db, user_id=user_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
