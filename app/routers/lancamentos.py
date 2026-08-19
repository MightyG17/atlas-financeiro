from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

from app.database import get_db
from app.models.lancamento import Lancamento
from app.models.usuario import Usuario
from app.services.auth_service import obter_usuario_atual

router = APIRouter()

# Schemas
class LancamentoCreate(BaseModel):
    tipo: str  # receita, despesa, transferencia
    categoria: str
    descricao: Optional[str] = None
    valor: Decimal
    data_lancamento: date
    data_vencimento: Optional[date] = None
    status: str = "pendente"

class LancamentoUpdate(BaseModel):
    tipo: Optional[str] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[Decimal] = None
    data_lancamento: Optional[date] = None
    data_vencimento: Optional[date] = None
    status: Optional[str] = None

class LancamentoResponse(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    categoria: str
    descricao: Optional[str]
    valor: Decimal
    data_lancamento: date
    data_vencimento: Optional[date]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=LancamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_lancamento(
    lancamento: LancamentoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    novo_lancamento = Lancamento(
        usuario_id=usuario.id,
        tipo=lancamento.tipo,
        categoria=lancamento.categoria,
        descricao=lancamento.descricao,
        valor=lancamento.valor,
        data_lancamento=lancamento.data_lancamento,
        data_vencimento=lancamento.data_vencimento,
        status=lancamento.status
    )
    db.add(novo_lancamento)
    db.commit()
    db.refresh(novo_lancamento)
    return novo_lancamento

@router.get("/", response_model=List[LancamentoResponse])
def listar_lancamentos(
    tipo: Optional[str] = None,
    categoria: Optional[str] = None,
    status: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    query = db.query(Lancamento).filter(Lancamento.usuario_id == usuario.id)

    if tipo:
        query = query.filter(Lancamento.tipo == tipo)
    if categoria:
        query = query.filter(Lancamento.categoria == categoria)
    if status:
        query = query.filter(Lancamento.status == status)
    if data_inicio:
        query = query.filter(Lancamento.data_lancamento >= data_inicio)
    if data_fim:
        query = query.filter(Lancamento.data_lancamento <= data_fim)

    lancamentos = query.offset(skip).limit(limit).all()
    return lancamentos

@router.get("/{lancamento_id}", response_model=LancamentoResponse)
def obter_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    lancamento = db.query(Lancamento).filter(
        Lancamento.id == lancamento_id,
        Lancamento.usuario_id == usuario.id
    ).first()

    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )
    return lancamento

@router.put("/{lancamento_id}", response_model=LancamentoResponse)
def atualizar_lancamento(
    lancamento_id: int,
    lancamento_update: LancamentoUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    lancamento = db.query(Lancamento).filter(
        Lancamento.id == lancamento_id,
        Lancamento.usuario_id == usuario.id
    ).first()

    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )

    for key, value in lancamento_update.dict(exclude_unset=True).items():
        setattr(lancamento, key, value)

    lancamento.updated_at = datetime.now()
    db.commit()
    db.refresh(lancamento)
    return lancamento

@router.delete("/{lancamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    lancamento = db.query(Lancamento).filter(
        Lancamento.id == lancamento_id,
        Lancamento.usuario_id == usuario.id
    ).first()

    if not lancamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lançamento não encontrado"
        )

    db.delete(lancamento)
    db.commit()
    return None

@router.get("/resumo/periodo")
def resumo_periodo(
    data_inicio: date,
    data_fim: date,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    lancamentos = db.query(Lancamento).filter(
        Lancamento.usuario_id == usuario.id,
        Lancamento.data_lancamento >= data_inicio,
        Lancamento.data_lancamento <= data_fim,
        Lancamento.status != "cancelado"
    ).all()

    total_receitas = sum(l.valor for l in lancamentos if l.tipo == "receita")
    total_despesas = sum(l.valor for l in lancamentos if l.tipo == "despesa")
    saldo = total_receitas - total_despesas

    return {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    }