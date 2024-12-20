from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.database import User, engine
import hashlib
import uuid

Session = sessionmaker(bind=engine)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    session = Session()
    try:
        hashed_password = hash_password(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()

def authenticate_user(username, password):
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and user.password == hash_password(password):
            return user.id
        return None
    finally:
        session.close()
