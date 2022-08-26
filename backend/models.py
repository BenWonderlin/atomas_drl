from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, LargeBinary
from sqlalchemy.sql import func

from database import Base


class Game(Base):

    __tablename__ = "games"

    id = Column(Integer, primary_key = True, index = True)

    object = Column(LargeBinary)
    score = Column(Integer)
    player_name = Column(String)

    center_element = Column(String)
    ring_elements = Column(String)
    turns_taken = Column(Integer)

    active_flag = Column(Boolean)
    assisted_flag = Column(Boolean)

    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())


