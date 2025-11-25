# Importing necessary libraries
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from src.main import SessionLocal

# Setting base class for database models
Base = declarative_base()

# Defining base class for user models
class UserBase(BaseModel):
    """Base class for user models"""
    email: str






    password: str  # Consider using bcrypt or another secure method for storing passwords
    nombre: str
    apellido: str

# Defining database model for users
class User(Base):
    """Database model for users"""
    __tablename__ = "users"  # Define table name
    id = Column(Integer, primary_key=True)  # Define primary key
    email = Column(String, unique=True)  # Define email
    password = Column(String)  # Store passwords securely
    nombre = Column(String)  # Define nombre
    apellido = Column(String)  # Define apellido

    # Configure pydantic to work with SQLAlchemy
    class Config:
        orm_mode = True

# Defining model for user creation
class UserCreate(UserBase):
    """Model for user creation"""
    class Config:
        orm_mode = True