from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.types import Float
from sqlalchemy.sql import func
from app.database import Base

class FaturaEnergia(Base):
    __tablename__ = "fatura_energia"

    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("contrato_energia.id"), nullable=False)
    mes_referencia = Column(Date, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    codigo_barras = Column(String(50), nullable=True)
    numero_fatura = Column(String(50), nullable=True)
    consumo_kwh = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)
    valor_tusd = Column(Float, nullable=True)
    valor_te = Column(Float, nullable=True)
    valor_bandeira = Column(Float, nullable=True)
    valor_iluminacao_publica = Column(Float, nullable=True)
    valor_icms = Column(Float, nullable=True)
    valor_pis_cofins = Column(Float, nullable=True)
    valor_contribuicao = Column(Float, nullable=True)
    bandeira_ativa = Column(String(20), nullable=True)
    fk_analise = Column(Integer, nullable=True)
    status = Column(String(20), default="pendente")
    data_pagamento = Column(Date, nullable=True)
    arquivo_original = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())