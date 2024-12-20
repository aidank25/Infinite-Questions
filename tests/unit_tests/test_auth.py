import pytest
from app.auth import register_user, authenticate_user
from app.database import Base, engine

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_user_registration():
    assert register_user("testuser", "password123")
    assert not register_user("testuser", "password123")  # Duplicate username

def test_user_authentication():
    register_user("testuser", "password123")
    assert authenticate_user("testuser", "password123") is not None
    assert authenticate_user("testuser", "wrongpass") is None
    assert authenticate_user("nonexistent", "password123") is None
