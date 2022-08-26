from typing import List, Union
from datetime import datetime
from pydantic import BaseModel


class GameBase(BaseModel):
    pass

class Game(GameBase):

    id: int
    score: int
    player_name: Union[str, None]

    center_element: Union[int, None]
    ring_elements: Union[str, None]
    turns_taken: int

    terminal: bool
    ai_assisted: bool

    created_at: Union[datetime, None]
    updated_at: Union[datetime, None]

    class Config:
        orm_mode = True


