from sqlalchemy import Column, Integer, String
from app.database import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
