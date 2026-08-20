import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app.routers import (
    auth,
    router_caixa,
    router_faturas,
    router_grupos,
    router_energia,
    lancamentos,
    contabilidade,
)

# 1. Cria as tabelas no banco de dados automaticamente
Base.metadata.create_all(bind=engine)

# 2. Instancia a aplicação ÚNICA
app = FastAPI(
    title="Atlas Financeiro API",
    version="3.0.0",
    description="Plataforma contábil de gestão financeira",
)

# 3. Lista de origens permitidas (Substitui o "*" para evitar bloqueio do navegador)
origins = [
    "https://atlas-financeiro-4hk9.onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5500",  # Para quando rodar com Live Server local
]

# 4. Configuração estrita do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.onrender\.com", # Permite qualquer subdomínio do Render
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 5. Mapeia a pasta do frontend apenas se ela existir no projeto
if os.path.exists("frontend"):
    app.mount(
        "/frontend", StaticFiles(directory="frontend", html=True), name="frontend"
    )

# 6. Registro de Routers
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(router_caixa.router, prefix="/caixa", tags=["Caixa"])
app.include_router(router_faturas.router, prefix="/faturas", tags=["Faturas"])
app.include_router(router_grupos.router, prefix="/grupos", tags=["Grupos"])
app.include_router(router_energia.router)
app.include_router(
    lancamentos.router, prefix="/lancamentos", tags=["Lançamentos"]
)
app.include_router(
    contabilidade.router, prefix="/contabilidade", tags=["Contabilidade"]
)


# 7. Rotas de teste e status
@app.get("/")
def root():
    return {
        "message": "Atlas Financeiro API",
        "version": "3.0.0",
        "status": "online",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}