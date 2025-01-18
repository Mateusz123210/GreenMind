from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("app/certs/users_url.txt") as f:
    url = f.readline().rstrip()

SQLALCHEMY_DATABASE_URL = url

users_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=2,
    max_overflow=0
)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=users_engine)

UsersBase = declarative_base()