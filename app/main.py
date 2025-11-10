from fastapi import FastAPI
from app.routes import users
from app.routes import transactions
from app.routes import portfolio
from app import models
from app.database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="WealthWise Portfolio Tracker API")

# Include routes
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(portfolio.router)

@app.get("/")
def root():
    return {"message": "Welcome to WealthWise Portfolio Tracker API"}
