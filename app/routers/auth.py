from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.database import get_db
from app.models.usuario import Usuario
from app.services.auth_service import hash_senha, verificar_senha, criar_token, decodificar_token
from app.config import SECRET_KEY, JWT_ALGORITHM

router = APIRouter()
security = HTTPBearer()

# Schemas
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    nome: str
    email: str

# Endpoints
@router.post("/cadastrar", response_model=TokenResponse)
def cadastrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se email já existe
    existing = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )

    # Cria novo usuário
    senha_hash = hash_senha(usuario.senha)
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash,
        created_at=datetime.now()
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # Gera token
    token = criar_token(
        {"sub": str(novo_usuario.id), "email": novo_usuario.email},
        SECRET_KEY,
        JWT_ALGORITHM
    )

    return TokenResponse(
        access_token=token,
        usuario_id=novo_usuario.id,
        nome=novo_usuario.nome,
        email=novo_usuario.email
    )

@router.post("/login", response_model=TokenResponse)
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    # Busca usuário
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )

    # Verifica senha
    if not verificar_senha(usuario.senha, db_usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )

    # Gera token
    token = criar_token(
        {"sub": str(db_usuario.id), "email": db_usuario.email},
        SECRET_KEY,
        JWT_ALGORITHM
    )

    return TokenResponse(
        access_token=token,
        usuario_id=db_usuario.id,
        nome=db_usuario.nome,
        email=db_usuario.email
    )

@router.get("/me")
def me(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decodificar_token(token, SECRET_KEY, JWT_ALGORITHM)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    usuario_id = int(payload.get("sub", 0))
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "created_at": usuario.created_at
    }