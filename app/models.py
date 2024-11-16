from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    last_login_attempt = Column(DateTime, nullable=False)

    user_tokens = relationship("Token", back_populates="users")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)
    access_token = Column(String, nullable=False)
    access_token_expiration_time = Column(DateTime, nullable=False)
    refresh_token = Column(String, nullable=False)
    refresh_token_expiration_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    users = relationship("User", back_populates="user_tokens")