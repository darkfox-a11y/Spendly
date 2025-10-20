from sqlalchemy import Column, Integer, String, ForeignKey,Numeric,Boolean,Date
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime,date


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_password = Column(String, nullable = False)

    #one to many relationship with subscriptions
    subscriptions = relationship("Subscription", back_populates="owner")
    #one to one relationship with budget
    budget = relationship("Budget", back_populates="user", uselist=False)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, index = True, nullable = False)
    description = Column(String, nullable = True)
    price = Column(Numeric(10,2), nullable = False)
    renewal_date = Column(Date, nullable = False)
    category = Column(String, nullable = False)

    owner_id = Column(Integer, ForeignKey("users.id"))#foreig key to connect to user table
    owner = relationship("User", back_populates="subscriptions")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    monthly_limit = Column(Numeric(10, 2), nullable=False)
    current_spent = Column(Numeric(10, 2), default=0.00)
    allow_over_limit = Column(Boolean, default=False)


    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("User", back_populates="budget")

