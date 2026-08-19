from fastapi import APIRouter, Depends, HTTPException
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

class ResumoCaixaResponse(BaseModel):
    saldo_total: Decimal
    total_receitas: Decimal
    total_despesas: Decimal
    data_referencia: date

@router.get("/resumo")
def resumo_caixa(
    data_referencia: Optional[date] = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    if not data_referencia:
        data_referencia = date.today()

    lancamentos = db.query(Lancamento).filter(
        Lancamento.usuario_id == usuario.id,
        Lancamento.data_lancamento <= data_referencia,
        Lancamento.status != "cancelado"
    ).all()

    total_receitas = sum(l.valor for l in lancamentos if l.tipo == "receita")
    total_despesas = sum(l.valor for l in lancamentos if l.tipo == "despesa")
    saldo = total_receitas - total_despesas

    return ResumoCaixaResponse(
        saldo_total=saldo,
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        data_referencia=data_referencia
    )