from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import string

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

@app.get('/random')
async def get_random_number():
    number = random.randint(1, 100)
    return {"random number": str(number)}

@app.get('/random-letter')
async def get_random_number():
    letter = random.choice(string.ascii_letters)
    return {"random letter": letter}
