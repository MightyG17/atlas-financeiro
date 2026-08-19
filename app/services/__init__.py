from app.services.auth_service import (
    AuthService,
    hash_senha,
    verificar_senha,
    criar_token,
    decodificar_token,
    autenticar_usuario,
    obter_usuario_atual
)

from app.services.ocr_energia import OCRService