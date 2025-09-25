from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

"""
Module de connexion à la base de données PostgreSQL.
Ce module utilise SQLAlchemy pour établir une connexion à la base de données PostgreSQL.
==> Contient la configuration et l’objet de connexion SQLAlchemy (c'est la "source de vérité").
"""

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# connexion à postgreSQL
HOST = "postgres"
USER = os.getenv("POSTGRES_USER")
DATABASE = os.getenv("POSTGRES_DB")
PORT = 5432
PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Vérifier si toutes les variables d'environnement sont définies
if not all([HOST, USER, DATABASE, PORT, PASSWORD]):
    raise ValueError("Une ou plusieurs variables d'environnement ne sont pas définies.")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Créer un engine SQLAlchemy
engine = create_engine(DATABASE_URL)#, echo = True) # echo=True pour afficher les requêtes SQL dans la console

# Créer un session maker SQLAlchemy
SessionLocal = sessionmaker(bind=engine)

# Créer une base ORM pour déclarer les modèles
class Base(DeclarativeBase):
    pass
