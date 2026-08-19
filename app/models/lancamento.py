from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.sql import func
from app.database import Base

class Lancamento(Base):
    __tablename__ = "lancamentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    perfil_id = Column(Integer, ForeignKey("perfis_financeiros.id"), nullable=True)
    tipo = Column(String(20), nullable=False)
    categoria = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    valor = Column(DECIMAL(15, 2), nullable=False)
    data_lancamento = Column(Date, nullable=False)
    data_vencimento = Column(Date, nullable=True)
    status = Column(String(20), default="pendente")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())