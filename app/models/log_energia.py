from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class LogEnergia(Base):
    __tablename__ = "log_energia"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    acao = Column(String(100), nullable=False)
    detalhes = Column(Text, nullable=True)
    ip_origem = Column(String(45), nullable=True)
    created_at = Column(DateTime, server_default=func.now())