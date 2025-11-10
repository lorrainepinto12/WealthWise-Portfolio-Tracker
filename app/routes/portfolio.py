from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

@router.get("/summary", response_model=schemas.PortfolioSummary, summary="Get portfolio summary", description="Fetch holdings, total value, and gains for a user")
def get_portfolio_summary(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists first
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        summary = crud.get_portfolio_summary(db, user_id=user_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
