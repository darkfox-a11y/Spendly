from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

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
    price = Column(Integer, nullable = False)
    renewal_date = Column(String, nullable = False)
    category = Column(String, nullable = False)

    owner_id = Column(Integer, ForeignKey("users.id"))#foreig key to connect to user table
    owner = relationship("User", back_populates="subscriptions")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key = True, index = True)
    monthly_limit = Column(Integer, nullable = False)
    current_spent = Column(Integer, default = 0.0)

    user = relationship("User", back_populates="budget")

