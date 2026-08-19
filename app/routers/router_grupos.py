from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

from app.database import get_db
from app.models.grupo_evento import GrupoEvento
from app.models.participante_grupo import ParticipanteGrupo
from app.models.despesa_grupo import DespesaGrupo
from app.models.usuario import Usuario
from app.services.auth_service import obter_usuario_atual

router = APIRouter()

class GrupoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    data_inicio: date
    data_fim: Optional[date] = None

class GrupoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    status: Optional[str] = None

class GrupoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    data_inicio: date
    data_fim: Optional[date]
    status: str
    criado_por: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

@router.post("/", response_model=GrupoResponse, status_code=status.HTTP_201_CREATED)
def criar_grupo(
    grupo: GrupoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    novo_grupo = GrupoEvento(
        nome=grupo.nome,
        descricao=grupo.descricao,
        data_inicio=grupo.data_inicio,
        data_fim=grupo.data_fim,
        criado_por=usuario.id,
        status="ativo"
    )
    db.add(novo_grupo)
    db.commit()
    db.refresh(novo_grupo)

    # Adiciona o criador como participante admin
    participante = ParticipanteGrupo(
        grupo_id=novo_grupo.id,
        usuario_id=usuario.id,
        papel="admin"
    )
    db.add(participante)
    db.commit()

    return novo_grupo

@router.get("/", response_model=List[GrupoResponse])
def listar_grupos(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    # Busca grupos onde o usuário é participante
    participantes = db.query(ParticipanteGrupo).filter(
        ParticipanteGrupo.usuario_id == usuario.id
    ).all()

    grupo_ids = [p.grupo_id for p in participantes]

    query = db.query(GrupoEvento).filter(GrupoEvento.id.in_(grupo_ids))
    if status:
        query = query.filter(GrupoEvento.status == status)

    return query.offset(skip).limit(limit).all()