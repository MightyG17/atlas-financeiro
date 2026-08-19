from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.sql import func
from app.database import Base

class DespesaGrupo(Base):
    __tablename__ = "despesas_grupo"

    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos_eventos.id"), nullable=False)
    descricao = Column(Text, nullable=False)
    valor = Column(DECIMAL(15, 2), nullable=False)
    data_despesa = Column(Date, nullable=False)
    categoria = Column(String(100), nullable=True)
    pago_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())