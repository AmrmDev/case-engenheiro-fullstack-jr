from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models
from backend.app.schemas import GameOut, AttemptCreate, AttemptResult, RankingEntry
from backend.app.auth import get_current_user
from backend.app.services.game_service import start_game, submit_attempt

router = APIRouter(prefix="/api/games", tags=["games"])

@router.post("/", response_model=GameOut, status_code=status.HTTP_201_CREATED)
def new_game(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return start_game(current_user.id, db)