# create_tables.py
from app.db.database import engine, Base
from app.db.models import User, Subscription, Budget

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")