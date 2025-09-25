from .database import Base
from .database import engine
def create_db_simple():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db_simple()