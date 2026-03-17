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


@router.post("/{game_id}/attempts", response_model=AttemptResult)
def attempt(
    game_id: int,
    attempt_data: AttemptCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    game = db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.user_id == current_user.id
    ).first()
    if not game:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    if len(attempt_data.guess) != 4:
        raise HTTPException(status_code=400, detail="O palpite deve ter exatamente 4 cores")

    result = submit_attempt(game_id, attempt_data.guess, db)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result