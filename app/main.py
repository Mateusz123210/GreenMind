from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.schemas import *
from app import services
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/register')
async def register(data: Login):
    return services.register(data)

@app.post('/login')
async def login(data: Login):
    return services.login(data)

@app.post('/logout')
async def logout(accessToken: str, email: str):
    return services.logout(accessToken, email)

@app.post('/refresh-token')
async def refresh_token(refreshToken: str, email: str):
    return services.refresh_token(refreshToken, email)

@app.delete('/account')
async def delete_account(accessToken: str, email: str):
    return services.delete_account(accessToken, email)
