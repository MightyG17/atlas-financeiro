from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

from app.database import get_db
from app.models.plano_conta import PlanoConta
from app.models.lancamento import Lancamento
from app.models.usuario import Usuario
from app.services.auth_service import obter_usuario_atual

router = APIRouter()

# Schemas
class PlanoContaCreate(BaseModel):
    codigo: str
    nome: str
    tipo: str  # ativo, passivo, receita, despesa
    pai_id: Optional[int] = None
    nivel: int = 1

class PlanoContaResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    tipo: str
    pai_id: Optional[int]
    nivel: int
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class BalancoPeriodoResponse(BaseModel):
    total_receitas: Decimal
    total_despesas: Decimal
    saldo: Decimal
    data_inicio: date
    data_fim: date

# Endpoints de Plano de Contas
@router.post("/plano-contas", response_model=PlanoContaResponse, status_code=status.HTTP_201_CREATED)
def criar_plano_conta(
    conta: PlanoContaCreate,
    db: Session = Depends(get_db)
):
    # Verifica se código já existe
    existing = db.query(PlanoConta).filter(PlanoConta.codigo == conta.codigo).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de conta já existe"
        )

    nova_conta = PlanoConta(
        codigo=conta.codigo,
        nome=conta.nome,
        tipo=conta.tipo,
        pai_id=conta.pai_id,
        nivel=conta.nivel
    )
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)
    return nova_conta

@router.get("/plano-contas", response_model=List[PlanoContaResponse])
def listar_plano_contas(
    tipo: Optional[str] = None,
    ativo: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(PlanoConta).filter(PlanoConta.ativo == ativo)
    if tipo:
        query = query.filter(PlanoConta.tipo == tipo)
    return query.order_by(PlanoConta.codigo).all()

@router.get("/balanco-periodo", response_model=BalancoPeriodoResponse)
def balanco_periodo(
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

    return BalancoPeriodoResponse(
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo,
        data_inicio=data_inicio,
        data_fim=data_fim
    )