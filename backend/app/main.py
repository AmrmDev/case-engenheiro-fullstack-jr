from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth_routes, game_routes

app = FastAPI(
    title="Mastermind API - Case JR",
    description="API backend do jogo Mastermind - Case Eng Full-Stack JR",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(game_routes.router)

@app.get("/")
def root():
    return {"message": "up"}