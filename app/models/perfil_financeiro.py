from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.types import DECIMAL
from sqlalchemy.sql import func
from app.database import Base

class PerfilFinanceiro(Base):
    __tablename__ = "perfis_financeiros"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    saldo_inicial = Column(DECIMAL(15, 2), default=0.00)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())