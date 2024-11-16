from datetime import datetime, timedelta, UTC
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day
ALGORITHM = "HS256"

def create_access_token(subject: Union[str, Any], jwt_secret_key: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        expires_delta = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], jwt_refresh_secret_key: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(UTC) + expires_delta
    else:
        expires_delta = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, jwt_refresh_secret_key, ALGORITHM)
    return encoded_jwt