from .database import Base

def create_db_simple():
    Base.metadata.create_all()

if __name__ == "__main__":
    create_db_simple()