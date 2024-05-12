#!/usr/bin/python3
"""
This module contains the ORM for our database
"""
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import PasswordType
from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """The base class for all ORM tables"""
    pass


class BaseModel():
    """The basemodel for all table ORM"""
    id = Column(UUID, default=uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class User(BaseModel, Base):
    """The user table ORM"""
    __tablename__ = "users"
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    middlename = Column(String(100), nullable=True)
    email = Column(EmailType, nullable=False, unique=True)
    password = Column(PasswordType(schemes="md5_crypt"), nullable=False)
    username = Column(String(100), nullable=False, unique=True)