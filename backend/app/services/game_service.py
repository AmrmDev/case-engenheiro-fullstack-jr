import json
import random
from datetime import datetime
from sqlalchemy.orm import Session
from app import models

COLORS = ["A", "B", "C", "D", "E", "F"]
CODE_LENGTH = 4
MAX_ATTEMPTS = 10

def generate_secret() -> list[str]:
    return random.sample(COLORS, CODE_LENGTH)

def check_attempt(secret: list[str], guess: list[str]) -> int:
    return sum(s == g for s, g in zip(secret, guess))

def calculate_score(attempts_count: int, duration_seconds: int) -> int:
    return max(0, 1000 - (attempts_count * 80) - (duration_seconds * 2))

def start_game(user_id: int, db: Session) -> models.Game:
    secret = generate_secret()
    game = models.Game(
        user_id=user_id,
        secret_code=json.dumps(secret),
        attempts_matrix="[]"
    )

    db.Add(game)
    db.commit()
    db.refresh(game)
    return game

def submit_attempt(game_id: int, guess: list[str], db: Session) -> dict:
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        return {"error": "Partida não encontrada"}
    if game.finished:
        return {"error": "Partida já finalizada"}

    secret = json.loads(game.secret_code)
    attempts = json.loads(game.attempts_matrix)
    attempt_number = len(attempts) + 1

    exact_hits = check_attempt(secret, guess)
    won = exact_hits == CODE_LENGTH
    game_over = won or attempt_number >= MAX_ATTEMPTS

    attempt = models.Attempt(
        game_id=game_id,
        guess=json.dumps(guess),
        exact_hits=exact_hits
    )
    db.add(attempt)

    attempts.append({"attempt": attempt_number, "guess": guess, "exact_hits": exact_hits})
    game.attempts_matrix = json.dumps(attempts)

    if game_over:
        game.finished = True
        game.won = won
        duration = int((datetime.utcnow() - game.created_at).total_seconds())
        game.duration_seconds = duration
        game.score = calculate_score(attempt_number, duration) if won else 0

        user = db.query(models.User).filter(models.User.id == game.user_id).first()
        if game.score > user.best_score:
            user.best_score = game.score

    db.commit()

    return {
        "attempt_number": attempt_number,
        "exact_hits": exact_hits,
        "game_over": game_over,
        "won": won,
        "score": game.score if game_over else None
    }