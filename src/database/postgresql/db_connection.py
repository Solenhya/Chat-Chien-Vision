from .database import SessionLocal
from sqlalchemy import text
from contextlib import contextmanager

#Fonction a utiliser
@contextmanager
def get_session():
    """create a new session to the database"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise #relance l’erreur après rollback
    finally:
        db.close()
