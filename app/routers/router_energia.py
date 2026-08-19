from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

from app.database import get_db
from app.models.contrato_energia import ContratoEnergia
from app.models.fatura_energia import FaturaEnergia
from app.models.analise_fatura_energia import AnaliseFaturaEnergia
from app.models.tarifa_bandeira import TarifaBandeira
from app.models.log_energia import LogEnergia
from app.models.usuario import Usuario
from app.services.auth_service import obter_usuario_atual

router = APIRouter(prefix="/api/v1/energia", tags=["Energia"])

# Schemas
class ContratoCreate(BaseModel):
    numero_contrato: str
    concessionaria: str
    unidade_consumidora: str
    modalidade_tarifaria: str
    tensao: str
    subgrupo: Optional[str] = None
    data_inicio: date
    data_fim: Optional[date] = None

class ContratoResponse(BaseModel):
    id: int
    usuario_id: int
    numero_contrato: str
    concessionaria: str
    unidade_consumidora: str
    modalidade_tarifaria: str
    tensao: str
    subgrupo: Optional[str]
    data_inicio: date
    data_fim: Optional[date]
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class FaturaEnergiaCreate(BaseModel):
    contrato_id: int
    mes_referencia: date
    data_vencimento: date
    codigo_barras: Optional[str] = None
    numero_fatura: Optional[str] = None
    consumo_kwh: float
    valor_total: float
    valor_tusd: Optional[float] = None
    valor_te: Optional[float] = None
    valor_bandeira: Optional[float] = None
    valor_iluminacao_publica: Optional[float] = None
    valor_icms: Optional[float] = None
    valor_pis_cofins: Optional[float] = None
    valor_contribuicao: Optional[float] = None
    bandeira_ativa: Optional[str] = None
    status: str = "pendente"

class FaturaEnergiaResponse(BaseModel):
    id: int
    contrato_id: int
    mes_referencia: date
    data_vencimento: date
    codigo_barras: Optional[str]
    numero_fatura: Optional[str]
    consumo_kwh: float
    valor_total: float
    valor_tusd: Optional[float]
    valor_te: Optional[float]
    valor_bandeira: Optional[float]
    valor_iluminacao_publica: Optional[float]
    valor_icms: Optional[float]
    valor_pis_cofins: Optional[float]
    valor_contribuicao: Optional[float]
    bandeira_ativa: Optional[str]
    fk_analise: Optional[int]
    status: str
    data_pagamento: Optional[date]
    arquivo_original: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class AnaliseEnergiaResponse(BaseModel):
    id: int
    fatura_id: int
    consumo_mes_anterior: Optional[float]
    consumo_mes_atual: Optional[float]
    variacao_consumo: Optional[float]
    valor_mes_anterior: Optional[float]
    valor_mes_atual: Optional[float]
    variacao_valor: Optional[float]
    consumo_medio_ultimos_3: Optional[float]
    consumo_medio_ultimos_6: Optional[float]
    consumo_medio_ultimos_12: Optional[float]
    preco_medio_kwh: Optional[float]
    tarifa_mais_vantajosa: Optional[str]
    economia_potencial: Optional[float]
    alertas: Optional[str]
    recomendacoes: Optional[str]
    data_analise: date
    created_at: datetime

    class Config:
        from_attributes = True

# Endpoints - Contratos
@router.post("/contratos", response_model=ContratoResponse, status_code=status.HTTP_201_CREATED)
def criar_contrato(
    contrato: ContratoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    existing = db.query(ContratoEnergia).filter(
        ContratoEnergia.numero_contrato == contrato.numero_contrato
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Número de contrato já existe"
        )

    novo_contrato = ContratoEnergia(
        usuario_id=usuario.id,
        **contrato.dict()
    )
    db.add(novo_contrato)
    db.commit()
    db.refresh(novo_contrato)
    return novo_contrato

@router.get("/contratos", response_model=List[ContratoResponse])
def listar_contratos(
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    return db.query(ContratoEnergia).filter(
        ContratoEnergia.usuario_id == usuario.id,
        ContratoEnergia.ativo == ativo
    ).all()

@router.get("/contratos/{contrato_id}", response_model=ContratoResponse)
def obter_contrato(
    contrato_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    contrato = db.query(ContratoEnergia).filter(
        ContratoEnergia.id == contrato_id,
        ContratoEnergia.usuario_id == usuario.id
    ).first()
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )
    return contrato

# Endpoints - Faturas de Energia
@router.post("/faturas", response_model=FaturaEnergiaResponse, status_code=status.HTTP_201_CREATED)
def criar_fatura_energia(
    fatura: FaturaEnergiaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    # Verifica se o contrato pertence ao usuário
    contrato = db.query(ContratoEnergia).filter(
        ContratoEnergia.id == fatura.contrato_id,
        ContratoEnergia.usuario_id == usuario.id
    ).first()
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )

    nova_fatura = FaturaEnergia(**fatura.dict())
    db.add(nova_fatura)
    db.commit()
    db.refresh(nova_fatura)
    return nova_fatura

@router.get("/faturas", response_model=List[FaturaEnergiaResponse])
def listar_faturas_energia(
    contrato_id: Optional[int] = None,
    status: Optional[str] = None,
    mes_referencia: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    query = db.query(FaturaEnergia).join(
        ContratoEnergia,
        ContratoEnergia.id == FaturaEnergia.contrato_id
    ).filter(ContratoEnergia.usuario_id == usuario.id)

    if contrato_id:
        query = query.filter(FaturaEnergia.contrato_id == contrato_id)
    if status:
        query = query.filter(FaturaEnergia.status == status)
    if mes_referencia:
        query = query.filter(FaturaEnergia.mes_referencia == mes_referencia)

    return query.order_by(FaturaEnergia.mes_referencia.desc()).offset(skip).limit(limit).all()

@router.get("/faturas/{fatura_id}", response_model=FaturaEnergiaResponse)
def obter_fatura_energia(
    fatura_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    fatura = db.query(FaturaEnergia).join(
        ContratoEnergia,
        ContratoEnergia.id == FaturaEnergia.contrato_id
    ).filter(
        FaturaEnergia.id == fatura_id,
        ContratoEnergia.usuario_id == usuario.id
    ).first()

    if not fatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fatura não encontrada"
        )
    return fatura

@router.post("/faturas/upload")
def upload_fatura_energia(
    file: UploadFile = File(...),
    contrato_id: int = Form(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    # Verifica contrato
    contrato = db.query(ContratoEnergia).filter(
        ContratoEnergia.id == contrato_id,
        ContratoEnergia.usuario_id == usuario.id
    ).first()
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato não encontrado"
        )

    # Aqui você implementaria a lógica de upload e OCR
    # Por enquanto, apenas registra o upload
    log = LogEnergia(
        usuario_id=usuario.id,
        acao="UPLOAD_FATURA",
        detalhes=f"Arquivo: {file.filename}, Contrato: {contrato_id}"
    )
    db.add(log)
    db.commit()

    return {
        "message": "Upload recebido com sucesso",
        "filename": file.filename,
        "contrato_id": contrato_id
    }

# Endpoints - Análises
@router.get("/analises/{fatura_id}", response_model=AnaliseEnergiaResponse)
def obter_analise_fatura(
    fatura_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    analise = db.query(AnaliseFaturaEnergia).filter(
        AnaliseFaturaEnergia.fatura_id == fatura_id
    ).first()

    if not analise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Análise não encontrada para esta fatura"
        )
    return analise

@router.get("/tarifas-bandeira", response_model=List[dict])
def listar_tarifas_bandeira(
    ativo: bool = True,
    db: Session = Depends(get_db)
):
    tarifas = db.query(TarifaBandeira).filter(
        TarifaBandeira.ativo == ativo
    ).all()

    return [
        {
            "id": t.id,
            "bandeira": t.bandeira,
            "valor_kwh": t.valor_kwh,
            "data_inicio": t.data_inicio,
            "data_fim": t.data_fim
        }
        for t in tarifas
    ]

# Endpoint de Resumo
@router.get("/dashboard/resumo")
def resumo_energia(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual)
):
    # Total de contratos
    total_contratos = db.query(ContratoEnergia).filter(
        ContratoEnergia.usuario_id == usuario.id,
        ContratoEnergia.ativo == True
    ).count()

    # Últimas faturas
    ultimas_faturas = db.query(FaturaEnergia).join(
        ContratoEnergia,
        ContratoEnergia.id == FaturaEnergia.contrato_id
    ).filter(
        ContratoEnergia.usuario_id == usuario.id
    ).order_by(FaturaEnergia.mes_referencia.desc()).limit(5).all()

    return {
        "total_contratos": total_contratos,
        "ultimas_faturas": [
            {
                "id": f.id,
                "mes_referencia": f.mes_referencia,
                "valor_total": f.valor_total,
                "consumo_kwh": f.consumo_kwh,
                "status": f.status,
                "concessionaria": f.contrato.concessionaria if f.contrato else None
            }
            for f in ultimas_faturas
        ]
    }