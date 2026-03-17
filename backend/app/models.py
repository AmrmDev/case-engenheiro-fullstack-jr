from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    best_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    games = relationship("Game", back_populates="user")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    secret_code = Column(String, nullable=False)
    score = Column(Integer, default=0)
    duration_seconds = Column(Integer, default=0)
    attempts_matrix = Column(String, default="[]")
    finished = Column(Boolean, default=False)
    won = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="games")
    attempts = relationship("Attempt", back_populates="game")

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    guess = Column(String, nullable=False)  # JSON string ex: '["A","B","C","D"]'
    exact_hits = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="attempts")