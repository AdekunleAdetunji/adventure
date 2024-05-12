from datetime import datetime
from datetime import timedelta
from datetime import timezone
from jose import jwt
from jose import JWTError
from fastapi import HTTPException
from fastapi import status

SECRET_KEY = "811af6039851ab9d565879900836ef8b21dd988a35f43419c3255e4f2a60b7da"
ALGORITHM = "HS256"
EXPIRATION_DELTA = timedelta(minutes=2)

def create_token(data: dict, expiration: timedelta = EXPIRATION_DELTA):
    """function to generate token on user sign in"""
    to_encode = data.copy()
    expiration_time = datetime.now(timezone.utc) + expiration
    to_encode.update({"exp": expiration_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """function to check validate a toke"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if not payload.get("sub"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials, expired")
    