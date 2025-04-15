# models.py
from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    fullname = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
