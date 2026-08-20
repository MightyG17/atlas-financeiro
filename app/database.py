import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Carrega variáveis do arquivo .env (quando rodar localmente)
load_dotenv()

# 1. Tenta buscar a string de conexão completa (usada no Render / Aiven)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Se a variável DATABASE_URL não existir, monta a URL com o banco local ou SQLite
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "atlas_financeiro")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # Conexão MySQL local
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Correção de compatibilidade para PostgreSQL (Postgres no Render/Aiven exige o driver no prefixo)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

# Configurações do Engine do SQLAlchemy
engine_args = {}

# O argumento check_same_thread só deve ser aplicado se o banco for SQLite
if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()