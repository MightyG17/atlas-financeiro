from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class ParticipanteGrupo(Base):
    __tablename__ = "participantes_grupo"

    id = Column(Integer, primary_key=True, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos_eventos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    papel = Column(String(50), default="membro")
    joined_at = Column(DateTime, server_default=func.now())