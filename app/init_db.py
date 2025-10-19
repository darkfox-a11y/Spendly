from app.db.database import Base, engine
from sqlalchemy import inspect

# Drop all existing tables safely
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

if existing_tables:
    print(f"Dropping tables: {existing_tables}")
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully.")

# Recreate all tables from current models
Base.metadata.create_all(bind=engine)
print("✅ Database schema recreated successfully.")
