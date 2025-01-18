from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("app/certs/plants_url.txt") as f:
    url = f.readline().rstrip()

SQLALCHEMY_DATABASE_URL = url

plants_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=2,
    max_overflow=0
)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=plants_engine)

PlantsBase = declarative_base()