from sqlalchemy.orm import sessionmaker
from app.database import Game, engine

Session = sessionmaker(bind=engine)

def create_game_record(user_id, word, num_questions, win=False):
    session = Session()
    try:
        game = Game(
            user_id=user_id,
            word=word,
            numQuestions=num_questions,
            win=win
        )
        session.add(game)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Error creating game record: {e}")
        return False
    finally:
        session.close()

def get_user_games(user_id):
    session = Session()
    try:
        games = session.query(Game)\
            .filter(Game.user_id == user_id)\
            .order_by(Game.created_at.desc())\
            .all()
        return games
    except Exception as e:
        print(f"Error retrieving games: {e}")
        return []
    finally:
        session.close()
