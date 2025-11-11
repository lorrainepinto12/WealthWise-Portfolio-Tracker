from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
import os


# Load environment variables from .env file
load_dotenv()

# Fetch the database URL 
DATABASE_URL = os.getenv("DATABASE_URL")

#Validate environment variable
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Please check your .env file.")

# Create SQLAlchemy engine to manage connections
try:
    engine = create_engine(DATABASE_URL)
except OperationalError as e:
    # Fail early if DB cannot connect
    raise RuntimeError(f"Cannot connect to database: {e}")

# SessionLocal class for database sessions
# Each request will use a fresh session for thread safety
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base() # All models will inherit from this

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
        # Propagates as 500 if the database is unreachable
        raise RuntimeError("Database connection error")
    finally:
            db.close()
