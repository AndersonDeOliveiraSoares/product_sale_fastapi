from fastapi import FastAPI
from app.api.router import api_router
from app.database import engine, Base
from app.middleware.error_handler import error_handler_middleware, setup_error_handlers
from app.api.v1.endpoints import analytics

# Garante a criação das tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Furniture Sales API - Enterprise Edition")

# --- CONFIGURAÇÃO DE ERROS (A ORDEM IMPORTA) ---
# 1. Handlers para erros de validação (Pydantic/Request)
setup_error_handlers(app)

# 2. Middleware para capturar exceções globais e de banco
app.middleware("http")(error_handler_middleware)

# --- ROTAS ---
app.include_router(api_router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "API Ativa e Monitorizada"}