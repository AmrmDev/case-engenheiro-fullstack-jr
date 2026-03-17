from __future__ import annotations
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# auth

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    best_score: int
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}
# game

class GameOut(BaseModel):
    id: int
    user_id: int
    score: int
    duration_seconds: int
    finished: bool
    won: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AttemptCreate(BaseModel):
    guess: list[str]  # ex: ["A", "B", "C", "D"]

class AttemptResult(BaseModel):
    attempt_number: int
    exact_hits: int
    game_over: bool
    won: bool
    score: Optional[int] = None

# rank

class RankingEntry(BaseModel):
    username: str
    best_score: int
    total_games: int

    class Config:
        from_attributes = True