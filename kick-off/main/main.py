#!/usr/bin/python3
"""The main module containing the fastapi application"""
from .engine import Engine
from .pydantic_model import UserRes
from .pydantic_model import UserSignUp
from .schema import User
from fastapi import FastAPI
from fastapi import Depends


app = FastAPI()


@app.post("/sign-up", response_model=UserRes)
async def sign_up(body: UserSignUp, engine: Engine = Depends(Engine())):
    """operation function to create a new user"""
    # deserialize the json data from pydantic
    data = body.model_dump()

    # supply the dic data to the engine post method
    print(data)
    user = engine.post(User, **data)
    print(user.__dict__)
    engine.save()
    # return success
    return user