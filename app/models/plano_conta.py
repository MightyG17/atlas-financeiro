from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base

class PlanoConta(Base):
    __tablename__ = "plano_contas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nome = Column(String(255), nullable=False)
    tipo = Column(String(20), nullable=False)
    pai_id = Column(Integer, ForeignKey("plano_contas.id"), nullable=True)
    nivel = Column(Integer, default=1)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())