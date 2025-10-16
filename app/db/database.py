from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
DATABASE_URL = os.getenv("DATABASE_URL")

# connect python to. postgresql database
engine = create_engine(DATABASE_URL)

#SessionLocal class is used to create a db session on every request 
SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #base class for our models to inherit from

#dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
