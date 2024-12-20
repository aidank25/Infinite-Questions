import pytest
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine, User, Game
from app.database.operations import create_game_record, get_user_games
import uuid

Session = sessionmaker(bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(setup_database):
    session = Session()
    yield session
    session.close()

def test_create_game_record(session):
    # Arrange
    user = User(id=str(uuid.uuid4()), username="testuser", password="password")
    session.add(user)
    session.commit()
    
    # Act
    result = create_game_record(user.id, "testword", 5, True)
    
    # Assert
    assert result == True
    game = session.query(Game).filter_by(user_id=user.id).first()
    assert game is not None
    assert game.word == "testword"
    assert game.numQuestions == 5
    assert game.win == True

def test_get_user_games(session):
    # Arrange
    user = User(id=str(uuid.uuid4()), username="testuser2", password="password")
    session.add(user)
    session.commit()
    create_game_record(user.id, "testword1", 3, False)
    create_game_record(user.id, "testword2", 7, True)
    
    # Act
    games = get_user_games(user.id)
    
    # Assert
    assert len(games) == 2
    assert games[0].word == "testword2"
    assert games[1].word == "testword1"
