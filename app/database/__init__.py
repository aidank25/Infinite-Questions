from sqlalchemy import create_engine, Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    games = relationship("Game", back_populates="user")


class Game(Base):
    __tablename__ = 'games'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    word = Column(String, nullable=False)
    numQuestions = Column(Integer, nullable=False)
    win = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="games")


# Create database engine
engine = create_engine('sqlite:///game.db')
Base.metadata.create_all(engine)