from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Enum
from .database import Base
import enum

class TodoState(enum.Enum):
    todo = 1
    doing = 2
    done = 3


class Todo(Base):
    __tablename__ = 'TB_TODO'

    id_ = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    description = Column(String(1024))
    state = Column(Enum(TodoState))

    def __init__(self, title, description, state):
        self.title = title
        self.description = description
        self.state = state

    def __repr__(self):
        return "<Todo('%s', '%s', '%s')>" % (self.title,
                                             self.description,
                                             self.state)
