from app.database import engine
from app import models

# This will create tables in the database
models.Base.metadata.create_all(bind=engine)

print("Tables created successfully!")

