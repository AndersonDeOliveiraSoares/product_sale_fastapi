from fastapi import FastAPI
from app.api.router import api_router
from app.database import engine, Base

# IMPORTANTE: Importe seus modelos aqui.
# Se você não importar, o SQLAlchemy não saberá quais tabelas criar.
from app.models import manufacturer

# Cria as tabelas automaticamente se elas não existirem
Base.metadata.create_all(bind=engine)
from app.api.v1.endpoints import analytics

app = FastAPI(title="Furniture Sales API")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API Rodando e Tabelas Verificadas!"}




app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])