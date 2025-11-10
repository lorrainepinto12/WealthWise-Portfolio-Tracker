from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.exc import OperationalError

# Load environment variables
load_dotenv()

# Fetch the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

#Validate environment variable
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Please check your .env file.")

# Create SQLAlchemy engine
try:
    engine = create_engine(DATABASE_URL)
except OperationalError as e:
    # Fail early if DB cannot connect
    raise RuntimeError(f"Cannot connect to database: {e}")

# SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()
# Dependency for FastAPI
def get_db():
    """
    Yield a database session for FastAPI dependency injection.
    Handles database connection errors centrally.
    """
    try:
        db = SessionLocal()
        yield db
    except OperationalError:
        # This will propagate to FastAPI as a 500
        raise RuntimeError("Database connection error")
    finally:
            db.close()
