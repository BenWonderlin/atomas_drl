import pickle

from typing import List
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from atomas.game_objs.AtomasRing import AtomasRing
from atomas.game_objs.RingElements import RingElement, Plus, Minus, Root

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import numpy as np
import tensorflow as tf
from tensorflow import keras

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

origins = [
    "http://localhost:5000",
    "https://deep-atomas.herokuapp.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/leaderboard", response_model = List[schemas.Game])
async def read_leaderboard(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    res = db.query(models.Game)\
        .filter(models.Game.player_name.is_not(None))\
        .filter(models.Game.terminal == True)\
        .order_by(models.Game.score.desc())\
        .offset(skip)\
        .limit(100)\
        .all()
    return res


@app.get("/games/{game_id}", response_model = schemas.Game)
async def read_game(game_id : int, db: Session = Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code = 404, detail = f"Game {game_id} not found")
    return db_game


@app.get("/new_game", response_model = schemas.Game)
async def create_game(db: Session = Depends(get_db)):

    ring = AtomasRing()

    db_game = models.Game(
        object = pickle.dumps(ring),
        center_element = ring.get_center_element().get_value(),
        ring_elements = ring.get_ring_str()
    )

    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


# action is query parameter
@app.put("/games/{game_id}", response_model = schemas.Game)
async def update_game(game_id : int, action : int, name = None, db: Session = Depends(get_db)):

    db_game = db.query(models.Game)\
        .filter(models.Game.id == game_id)\
        .first()

    if not db_game:
        raise HTTPException(status_code = 404, detail = f"Game {game_id} not found")

    ring = pickle.loads(db_game.object)
    if ring.get_terminal():
        if name:
            db_game.player_name = name
            db.commit()
            db.refresh(db_game)
        return db_game

    if action == -1:

        current_state, num_legal_actions, _, _ = ring.check()
        model = keras.models.load_model("dqn_model")

        current_state_tensor = tf.expand_dims(tf.convert_to_tensor(current_state), 0)
        q_values = model(current_state_tensor, training = False)
        
        action = tf.argmax(q_values[0][:num_legal_actions]).numpy()

    try:
        ring.take_turn(action)
    except ValueError:
        raise HTTPException(status_code = 400, detail = f"Invalid action syntax")
    except IndexError:
        raise HTTPException(status_code = 400, detail = f"Action index out of range")

    db_game.object = pickle.dumps(ring)
    db_game.score = ring.get_score()
    db_game.player_name = name
    
    db_game.center_element = ring.get_center_element().get_value() if ring.get_center_element() else None
    db_game.ring_elements = ring.get_ring_str()
    db_game.turns_taken = ring.get_turn_count()

    db_game.terminal = ring.get_terminal() 

    db.commit()
    db.refresh(db_game)

    return db_game