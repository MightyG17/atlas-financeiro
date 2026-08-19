import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import re

from app.database import get_db
from app.models.usuario import Usuario
from app.config import SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION

security = HTTPBearer()

class AuthService:
    @staticmethod
    def hash_senha(senha: str) -> str:
        """Gera hash bcrypt da senha"""
        # Converte para bytes e garante que não ultrapasse 72 bytes
        senha_bytes = senha.encode('utf-8')[:72]
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

    @staticmethod
    def verificar_senha(senha: str, senha_hash: str) -> bool:
        """Verifica se a senha corresponde ao hash"""
        try:
            senha_bytes = senha.encode('utf-8')[:72]
            return bcrypt.checkpw(senha_bytes, senha_hash.encode('utf-8'))
        except Exception:
            return False

    @staticmethod
    def criar_token(payload: Dict[str, Any], expiracao: Optional[int] = None) -> str:
        to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(seconds=expiracao or JWT_EXPIRATION)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decodificar_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def autenticar_usuario(email: str, senha: str, db: Session) -> Optional[Usuario]:
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if not usuario:
            return None
        if not AuthService.verificar_senha(senha, usuario.senha_hash):
            return None
        return usuario

def hash_senha(senha: str) -> str:
    return AuthService.hash_senha(senha)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return AuthService.verificar_senha(senha, senha_hash)

def criar_token(payload: Dict[str, Any], secret_key: str, algorithm: str, expiracao: Optional[int] = None) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(seconds=expiracao or JWT_EXPIRATION)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def decodificar_token(token: str, secret_key: str, algorithm: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.InvalidTokenError:
        return None

def autenticar_usuario(email: str, senha: str, db: Session) -> Optional[Usuario]:
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario

def obter_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
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

    return usuario