from datetime import datetime, timedelta
from typing import Optional, Dict, Union, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.config import AUTH_SECRET_KEY, AUTH_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SOFIA_API_KEY

# Esquemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []

# Contexto de seguridad para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sistema de seguridad
security = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT con los datos proporcionados.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)
    
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña proporcionada coincide con la almacenada hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para la contraseña proporcionada.
    """
    return pwd_context.hash(password)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Valida un token JWT y devuelve los datos del usuario.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, scopes=payload.get("scopes", []))
    except JWTError:
        raise credentials_exception
    
    # En un sistema real, aquí se verificaría el usuario contra una base de datos
    # Por ahora, simplemente devolvemos los datos del token
    return {"username": token_data.username, "scopes": token_data.scopes}

async def get_api_key(api_key: str = Depends(api_key_header)) -> Dict[str, Any]:
    """
    Valida una API Key y devuelve los datos asociados.
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key no proporcionada",
        )
    
    # Comprobar si es la API Key de SofIA
    if api_key == SOFIA_API_KEY:
        return {"client": "sofia", "scopes": ["read", "write"]}
    
    # Si no es una API Key válida
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API Key inválida",
    )

async def validate_access(
    credentials: Union[Dict[str, Any], None] = Depends(get_current_user),
    api_key: Union[Dict[str, Any], None] = Depends(get_api_key)
) -> Dict[str, Any]:
    """
    Valida el acceso mediante token JWT o API Key.
    """
    if credentials:
        return credentials
    
    if api_key:
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autenticación requerida",
    )

# Función para validar permisos específicos
def validate_scope(required_scope: str):
    """
    Crea un validador que comprueba si el usuario tiene un permiso específico.
    """
    async def validate_user_scope(user: Dict[str, Any] = Depends(validate_access)):
        if required_scope not in user.get("scopes", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso insuficiente. Se requiere: {required_scope}",
            )
        return user
    
    return validate_user_scope 