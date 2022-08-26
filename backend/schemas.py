
from datetime import datetime
from pydantic import BaseModel


class GameBase(BaseModel):
    pass

class Game(GameBase):

    id: int
    score: int
    player_name: str

    center_element: str
    ring_elements: str
    turns_taken: int

    active_flag: bool
    assisted_flag: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Action(BaseModel):
    action_num: int
    class Config:
        orm_mode = True
