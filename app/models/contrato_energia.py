from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.types import Float
from sqlalchemy.sql import func
from app.database import Base

class ContratoEnergia(Base):
    __tablename__ = "contrato_energia"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    numero_contrato = Column(String(50), unique=True, nullable=False)
    concessionaria = Column(String(255), nullable=False)
    unidade_consumidora = Column(String(50), nullable=False)
    modalidade_tarifaria = Column(String(50), nullable=False)
    tensao = Column(String(20), nullable=False)
    subgrupo = Column(String(20), nullable=True)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())