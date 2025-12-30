from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Nome do novo banco para evitar conflito
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user_fastapi:pass_fastapi@db_fastapi:5432/furniture_fastapi_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para injetar o banco nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()