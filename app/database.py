import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega variáveis do arquivo .env (local) ou do provedor de hospedagem
load_dotenv()

# 1. Busca a string de conexão completa (DATABASE_URL — Aiven / Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Se NÃO tiver DATABASE_URL → usa configurações separadas (MySQL local)
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "atlas_financeiro")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # Monta URL de conexão MySQL
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Correção obrigatória para PostgreSQL: adiciona o driver psycopg2
# O Aiven e muitos serviços usam "postgres://" mas SQLAlchemy precisa de "postgresql+psycopg2://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

# 4. Configurações específicas do Engine
engine_args = {}

# O argumento check_same_thread é EXCLUSIVO do SQLite — só aplica se for SQLite
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

# Cria a conexão com o banco
engine = create_engine(DATABASE_URL, **engine_args)

# Sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para todos os modelos
Base = declarative_base()


# Dependência para injetar a sessão do banco nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()