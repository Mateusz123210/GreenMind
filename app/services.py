from fastapi import HTTPException, status
from app import crud
from app.generators import jwt_token_generator
from app.utils import create_access_token, create_refresh_token
from datetime import datetime, UTC, timedelta
from app.schemas import *
from app import validating
from app.decorators.database import transactional
import pytz
from jose import jwt
from app.utils import (
    ALGORITHM
)
from pydantic import ValidationError
from app import hashing
from app.generators.uuid_generator import generate_uuid

@transactional
def register(data: Login):

    if validating.validate_email(data.email) is False:
        raise HTTPException(status_code=400, detail="Email has invalid format")
    
    db_user = crud.get_user_by_email(email=data.email)
    if db_user:
        raise HTTPException(status_code=409, detail="This email currently exists in app!")
        
    if validating.validate_password(data.password) is False:
        raise HTTPException(status_code=400, detail="Password has invalid format")
    
    hashed_password = hashing.hash_password(data.password)

    utc=pytz.UTC

    db_user = crud.create_user(email=data.email, password=hashed_password, 
                               last_login_attempt=datetime.now(UTC), uuid = generate_uuid())
                                  
    return {}

@transactional
def login(data: Login):
    
    if validating.validate_email(data.email) is False:
        raise HTTPException(status_code=400, detail="Email has invalid format")
    
    if validating.validate_password(data.password) is False:
        raise HTTPException(status_code=400, detail="Password has invalid format")
    
    db_user = crud.get_user_by_email(email=data.email)

    if db_user is None:
        raise HTTPException(status_code=409, detail="Invalid email or password!")
        
    hashed_password = hashing.hash_password(data.password)

    utc=pytz.UTC
    
    access_token_key = jwt_token_generator.generate_jwt_secret_key()

    while check_access_token_key(db_user, access_token_key) is False:
        access_token_key = jwt_token_generator.generate_jwt_secret_key()

    refresh_token_key = jwt_token_generator.generate_jwt_secret_key()

    while check_refresh_token_key(db_user, refresh_token_key) is False:
        refresh_token_key = jwt_token_generator.generate_jwt_secret_key()

    access_token = create_access_token(data.email, access_token_key)
    refresh_token = create_refresh_token(data.email, refresh_token_key)

    access_token_expiration_time = datetime.now(UTC) + timedelta(minutes=15)
    refresh_token_expiration_time = datetime.now(UTC) + timedelta(minutes=60*24)

    crud.login_user(db_user, access_token_key, access_token_expiration_time, refresh_token_key, 
                    refresh_token_expiration_time)
    
    utc=pytz.UTC

    if datetime.now(UTC) - timedelta(seconds = 0.5) <= utc.localize(db_user.last_login_attempt):
        raise HTTPException(status_code=429, detail="You are too fast! There is probability, that you are a robot.")
                                  
    return {"access_token": access_token, "refresh_token": refresh_token}

@transactional
def refresh_password(data: Email):
    raise HTTPException(status_code=501, detail="Not implemented yet!")

@transactional
def logout(access_token: str, email: str):
    db_user = crud.get_user_by_email(email=email)
    if db_user is None:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    db_user_tokens = crud.get_user_tokens(db_user)

    found = False
    expired = True
    found_token = None

    for db_token in db_user_tokens:
        try:
            payload = jwt.decode(
                access_token, db_token.access_token, algorithms=[ALGORITHM]
            )
            if payload["sub"] == email:
                found = True
                utc=pytz.UTC
                datetime_now = datetime.now(UTC)
                token_expiration_time = utc.localize(db_token.access_token_expiration_time)
                if datetime_now <= token_expiration_time:
                    expired = False    
                    found_token = db_token            
    
        except(jwt.JWTError, ValidationError):
            pass
        
    if found is False:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    if expired is True:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    crud.delete_token(found_token)
    return {}

@transactional
def refresh_token(refresh_token, email):
    db_user = crud.get_user_by_email(email=email)
    if db_user is None:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    db_user_tokens = crud.get_user_tokens(db_user)

    found_token = None
    found = False
    expired = True

    for db_token in db_user_tokens:

        try:
            payload = jwt.decode(
                refresh_token, db_token.refresh_token, algorithms=[ALGORITHM]
            )
            if payload["sub"] == email:
                found = True
                utc=pytz.UTC
                datetime_now = datetime.now(UTC)
                token_expiration_time = utc.localize(db_token.refresh_token_expiration_time)
                if datetime_now <= token_expiration_time:
                    expired = False       
                    found_token = db_token         
    
        except(jwt.JWTError, ValidationError):
            pass
        
    if found is False:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    if expired is True:

        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_key = jwt_token_generator.generate_jwt_secret_key()

    while check_access_token_key(db_user, access_token_key) is False:
        access_token_key = jwt_token_generator.generate_jwt_secret_key()

    refresh_token_key = jwt_token_generator.generate_jwt_secret_key()

    while check_refresh_token_key(db_user, refresh_token_key) is False:
        refresh_token_key = jwt_token_generator.generate_jwt_secret_key()

    access_token = create_access_token(email, access_token_key)
    refresh_token = create_refresh_token(email, refresh_token_key)

    access_token_expiration_time = datetime.now(UTC) + timedelta(minutes=15)
    refresh_token_expiration_time = datetime.now(UTC) + timedelta(minutes=60*24)

    crud.update_token(found_token, access_token_key, access_token_expiration_time, refresh_token_key,
                      refresh_token_expiration_time)

    return {"access_token": access_token, "refresh_token": refresh_token}

@transactional
def delete_account(access_token: str, email: str):

    db_user = crud.get_user_by_email(email=email)

    if db_user is None:

        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    db_user_tokens = crud.get_user_tokens(db_user)

    found = False
    expired = True
    found_token = None

    for db_token in db_user_tokens:
        try:
            payload = jwt.decode(
                access_token, db_token.access_token, algorithms=[ALGORITHM]
            )
            if payload["sub"] == email:
                found = True
                utc=pytz.UTC
                datetime_now = datetime.now(UTC)
                token_expiration_time = utc.localize(db_token.access_token_expiration_time)
                if datetime_now <= token_expiration_time:
                    expired = False    
                    found_token = db_token            
    
        except(jwt.JWTError, ValidationError):
            pass
        
    if found is False:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    if expired is True:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    crud.delete_user(db_user)

    return {}

@transactional
def delete_expired_tokens():

    tokens = crud.get_all_tokens()
    
    for token in tokens:

        utc=pytz.UTC
        datetime_now = datetime.now(UTC)
        token_expiration_time = utc.localize(token.refresh_token_expiration_time)

        if datetime_now > token_expiration_time:
            crud.delete_token(token)

def check_access_token_key(user, access_token_key):

    db_user_tokens = crud.get_user_tokens(user)

    for db_token in db_user_tokens:
        if db_token.access_token == access_token_key:

            return False
        
    return True

def check_refresh_token_key(user, refresh_token_key):

    db_user_tokens = crud.get_user_tokens(user)

    for db_token in db_user_tokens:
        if db_token.refresh_token == refresh_token_key:

            return False
        
    return True