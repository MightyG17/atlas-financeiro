from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from sqlalchemy.types import Float
from sqlalchemy.sql import func
from app.database import Base

class TarifaBandeira(Base):
    __tablename__ = "tarifa_bandeira"

    id = Column(Integer, primary_key=True, index=True)
    bandeira = Column(String(20), nullable=False)
    valor_kwh = Column(Float, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    ativo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())