from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Todos(Base):
    __tablename__= "todos"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    created = Column(String)
    completed = Column(Boolean)