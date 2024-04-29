#!/usr/bin/python3
"""
Pydantic model to serialize and deserialize user information
"""
from pydantic import BaseModel
from pydantic import EmailStr


class UserRes(BaseModel):
    """Model to validate and return user instance"""
    firstname: str
    lastname: str
    middlename: str | None
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class UserSignUp(UserRes):
    """Model to validate user sign up data"""
    password: str