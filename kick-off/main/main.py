#!/usr/bin/python3
"""The main module containing the fastapi application"""
from .engine import Engine
from .pydantic_model import Token
from .pydantic_model import UserRes
from .pydantic_model import UserSignUp
from .schema import User
from .token import create_token
from .token import verify_token
from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app = FastAPI()


@app.post("/sign-up", response_model=UserRes)
async def sign_up(body: UserSignUp, engine: Engine = Depends(Engine())):
    """operation function to create a new user"""
    # deserialize the json data from pydantic
    data = body.model_dump()

    # supply the dic data to the engine post method
    user = engine.post(User, **data)
    engine.save()
    return user


@app.post("/token", response_model=Token)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                engine: Engine = Depends(Engine())):
    """route to generate token"""
    username = form_data.username
    password = form_data.password
    user = engine.get_user(User, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="invalid password")
    data = {"sub": username}
    access_token = create_token(data)
    return Token(access_token=access_token, access_type="bearer")

@app.get("/users/{username}", response_model=UserRes)
async def get_user(token: Annotated[str, Depends(oauth2_scheme)],
                   username: str, engine: Engine = Depends(Engine())):
    """route to get a user information"""
    # verify token is still valid
    payload = verify_token(token)
    payload_user = payload.get("sub")
    if payload_user != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    # verify user still in database
    user = engine.get_user(User, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    # return user instance
    return user