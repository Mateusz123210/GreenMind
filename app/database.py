from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("app/certs/url.txt") as f:
    url = f.readline().rstrip()

SQLALCHEMY_DATABASE_URL = url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()