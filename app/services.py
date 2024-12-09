from fastapi import HTTPException
from fastapi.responses import Response
from app import crud
from app.schemas import *
from app.decorators.database import transactional

@transactional
def add_token(data: Token):
    
    token = crud.get_token(data.token)
    if token:
        raise HTTPException(status_code=400, detail="This token currently exists!")

    crud.add_token(token = data)
                                  
    return Response(status_code = 200)

@transactional
def delete_token(data: Token):
    
    token = crud.get_token(data.token)
    if token is None:
        raise HTTPException(status_code=4090, detail="This token does not exists!")

    crud.delete_token(token = token)

    return Response(status_code = 200)

@transactional
def delete_user(data: UserID):
    
    user_tokens = crud.get_user_tokens(user_id = data.user_id)

    if len(user_tokens) == 0:
        raise HTTPException(status_code=400, detail="User has no tokens!")
    
    crud.delete_user_tokens(user_tokens = user_tokens)

    return Response(status_code = 200)
