from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv as ld

from . import models
from .db import get_db

import os

ld("env\.env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev_test_key_to_change")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

password_ctx = CryptContext(schemes=["argon2", "bcrypt_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def password_hash(password:str) -> str:
    return password_ctx.hash(password)

def verify_hash(plain_password:str, hash: str) -> bool:
    return password_ctx.verify(plain_password, hash)

def create_token(data:dict, expires_delta: timedelta | None = None) -> str:
    encode_tgt = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    encode_tgt.update({"exp": expire})
    return jwt.encode(encode_tgt, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="No autorizado", headers={"WWW-Authenticate" : "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise credentials_exception

    return user

def require_admin(user: models.User = Depends(get_current_user)) -> models.User:

    if user.role != models.RoleEnum.admin:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Se requieren privilegios de administrador")
    
    return user

def require_teacher(user: models.User = Depends(get_current_user)) -> models.User:

    if user.role != models.RoleEnum.teacher or user.role != models.RoleEnum.admin:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Se requieren privilegios de profesor o administrador")

    return user
