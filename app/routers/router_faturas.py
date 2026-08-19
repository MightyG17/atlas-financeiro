from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

from app.database import get_db
from app.models.fatura_concessionaria import FaturaConcessionaria
from app.models.usuario import Usuario
from app.services.auth_service import obter_usuario_atual

router = APIRouter()

class FaturaCreate(BaseModel):
    codigo_barras: str
    valor: Decimal
    data_vencimento: date
    data_pagamento: Optional[date] = None
    status: str = "pendente"
    descricao: Optional[str] = None
    categoria: Optional[str] = None

class FaturaUpdate(BaseModel):
    valor: Optional[Decimal] = None
    data_vencimento: Optional[date] = None
    data_pagamento: Optional[date] = None
    status: Optional[str] = None
    descricao: Optional[str] = None
    categoria: Optional[str] = None

class FaturaResponse(BaseModel):
    id: int
    codigo_barras: str
    valor: Decimal
    data_vencimento: date
    data_pagamento: Optional[date]
    status: str
    descricao: Optional[str]
    categoria: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

@router.post("/", response_model=FaturaResponse, status_code=status.HTTP_201_CREATED)
def criar_fatura(
    fatura: FaturaCreate,
    db: Session = Depends(get_db)
):
    # Verifica se código de barras já existe
    existing = db.query(FaturaConcessionaria).filter(
        FaturaConcessionaria.codigo_barras == fatura.codigo_barras
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de barras já cadastrado"
        )

    nova_fatura = FaturaConcessionaria(**fatura.dict())
    db.add(nova_fatura)
    db.commit()
    db.refresh(nova_fatura)
    return nova_fatura

@router.get("/", response_model=List[FaturaResponse])
def listar_faturas(
    status: Optional[str] = None,
    data_vencimento_inicio: Optional[date] = None,
    data_vencimento_fim: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(FaturaConcessionaria)

    if status:
        query = query.filter(FaturaConcessionaria.status == status)
    if data_vencimento_inicio:
        query = query.filter(FaturaConcessionaria.data_vencimento >= data_vencimento_inicio)
    if data_vencimento_fim:
        query = query.filter(FaturaConcessionaria.data_vencimento <= data_vencimento_fim)

    return query.offset(skip).limit(limit).all()

@router.get("/{fatura_id}", response_model=FaturaResponse)
def obter_fatura(
    fatura_id: int,
    db: Session = Depends(get_db)
):
    fatura = db.query(FaturaConcessionaria).filter(FaturaConcessionaria.id == fatura_id).first()
    if not fatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fatura não encontrada"
        )
    return fatura

@router.put("/{fatura_id}", response_model=FaturaResponse)
def atualizar_fatura(
    fatura_id: int,
    fatura_update: FaturaUpdate,
    db: Session = Depends(get_db)
):
    fatura = db.query(FaturaConcessionaria).filter(FaturaConcessionaria.id == fatura_id).first()
    if not fatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fatura não encontrada"
        )

    for key, value in fatura_update.dict(exclude_unset=True).items():
        setattr(fatura, key, value)

    fatura.updated_at = datetime.now()
    db.commit()
    db.refresh(fatura)
    return fatura

@router.delete("/{fatura_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_fatura(
    fatura_id: int,
    db: Session = Depends(get_db)
):
    fatura = db.query(FaturaConcessionaria).filter(FaturaConcessionaria.id == fatura_id).first()
    if not fatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fatura não encontrada"
        )

    db.delete(fatura)
    db.commit()
    return None