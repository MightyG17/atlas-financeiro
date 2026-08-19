from sqlalchemy import Column, Integer, String, DateTime, Date, Text
from sqlalchemy.types import DECIMAL
from sqlalchemy.sql import func
from app.database import Base

class FaturaConcessionaria(Base):
    __tablename__ = "faturas_concessionarias"

    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String(50), unique=True, nullable=False)
    valor = Column(DECIMAL(15, 2), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    status = Column(String(20), default="pendente")
    descricao = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())