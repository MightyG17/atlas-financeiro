from sqlalchemy import Column, Integer, String, DateTime, Date, Text
from sqlalchemy.types import Float
from sqlalchemy.sql import func
from app.database import Base

class AnaliseFaturaEnergia(Base):
    __tablename__ = "analise_fatura_energia"

    id = Column(Integer, primary_key=True, index=True)
    fatura_id = Column(Integer, nullable=False)
    consumo_mes_anterior = Column(Float, nullable=True)
    consumo_mes_atual = Column(Float, nullable=True)
    variacao_consumo = Column(Float, nullable=True)
    valor_mes_anterior = Column(Float, nullable=True)
    valor_mes_atual = Column(Float, nullable=True)
    variacao_valor = Column(Float, nullable=True)
    consumo_medio_ultimos_3 = Column(Float, nullable=True)
    consumo_medio_ultimos_6 = Column(Float, nullable=True)
    consumo_medio_ultimos_12 = Column(Float, nullable=True)
    preco_medio_kwh = Column(Float, nullable=True)
    tarifa_mais_vantajosa = Column(String(50), nullable=True)
    economia_potencial = Column(Float, nullable=True)
    alertas = Column(Text, nullable=True)
    recomendacoes = Column(Text, nullable=True)
    data_analise = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())