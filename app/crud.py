from app import models
from app.schemas import *
from app.decorators.database import db

@db
def get_user_by_email(email: str, db):
    return db.query(models.User).filter(models.User.email == email).first()

@db
def get_all_tokens(db):
    return db.query(models.Token).all()

@db
def create_user(email, password, last_login_attempt, db):
    db_user = models.User(email=email, password=password, last_login_attempt=last_login_attempt)
    db.add(db_user)
    db.flush()

@db
def login_user(db_user, access_token, access_token_expiration_time, refresh_token, 
               refresh_token_expiration_time, db):
    db_token = models.Token(access_token=access_token, access_token_expiration_time=access_token_expiration_time,
                            refresh_token=refresh_token, refresh_token_expiration_time=refresh_token_expiration_time,
                            user_id=db_user.id)
    db.add(db_token)
    db.flush()

@db
def delete_user(user, db):
    user_tokens = db.query(models.Token).filter(models.Token.user_id==user.id)
    for token in user_tokens:
        db.delete(token)
    db.delete(user)
    db.flush()

@db
def delete_token(token: models.Token, db):
    db.delete(token)
    db.flush()

@db
def delete_user_tokens(user, db):
    user_tokens = db.query(models.Token).filter(models.Token.user_id==user.id)
    for token in user_tokens:
        db.delete(token)
    db.flush()

@db
def get_user_tokens(user, db):
    return db.query(models.Token).filter(models.Token.user_id == user.id).all()

@db
def update_token(found_token, access_token, access_token_expiration_time, refresh_token, 
                 refresh_token_expiration_time, db):
    db.query(models.Token).filter(models.Token.id==found_token.id).update({"access_token": access_token, 
                                "access_token_expiration_time": access_token_expiration_time,
                                "refresh_token": refresh_token, 
                                "refresh_token_expiration_time": refresh_token_expiration_time})
    db.flush()



