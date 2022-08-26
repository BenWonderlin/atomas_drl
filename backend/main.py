from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# origins = [
#     "http://localhost",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/leaderboard")
async def read_leaderboard():
    return {"doot" : "doot doot"}


@app.get("/games/{game_id}")
async def read_game(game_id : int):
    return {"game id": game_id}


@app.post("/games/{game_id}")
async def create_game(game_id : int):
    return {"game id": game_id}


# action is query parameter
@app.put("/games/{game_id}")
async def update_game(game_id : int, action_num : int):
    return {"game id": game_id, "action" : action_num}