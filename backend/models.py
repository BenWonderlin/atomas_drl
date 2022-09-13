from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary
from sqlalchemy.sql import func

from database import Base


class Game(Base):

    __tablename__ = "games"

    id = Column(Integer, primary_key = True, index = True)
    object = Column(LargeBinary)
    score = Column(Integer, default = 0)
    player_name = Column(String, default = None)

    center_element = Column(Integer, default = 0)
    ring_elements = Column(String, default = None)
    turns_taken = Column(Integer, default = 0)

    terminal = Column(Boolean, default = False)
    ai_assisted = Column(Boolean, default = False)
    human_assisted = Column(Boolean, default = False)

    created_at = Column(DateTime(timezone = True), default = func.now())
    updated_at = Column(DateTime(timezone = True), default = func.now(), onupdate = func.now())


