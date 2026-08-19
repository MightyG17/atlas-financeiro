from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Importa todos os routers disponíveis
from app.routers import auth
from app.routers import router_caixa
from app.routers import router_faturas
from app.routers import router_grupos
from app.routers import router_energia
from app.routers import lancamentos
from app.routers import contabilidade

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Atlas Financeiro API",
    version="3.0.0",
    description="Plataforma contábil de gestão financeira"
)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mapeia a pasta do frontend
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRO DOS ROUTERS

# Autenticação
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])

# Caixa, Faturas, Grupos, etc.
app.include_router(router_caixa.router, prefix="/caixa", tags=["Caixa"])
app.include_router(router_faturas.router, prefix="/faturas", tags=["Faturas"])
app.include_router(router_grupos.router, prefix="/grupos", tags=["Grupos"])

# Energia (com prefixo /api/v1/energia)
app.include_router(router_energia.router)

# Lançamentos e Contabilidade
app.include_router(lancamentos.router, prefix="/lancamentos", tags=["Lançamentos"])
app.include_router(contabilidade.router, prefix="/contabilidade", tags=["Contabilidade"])

@app.get("/")
def root():
    return {"message": "Atlas Financeiro API", "version": "3.0.0", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}