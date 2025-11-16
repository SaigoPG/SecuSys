
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import models, schemas, auth
from app.utils.db import get_db

router = APIRouter(prefix="/users",tags=["usuarios"])

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):

    exists = db.query(models.User).filter(models.User.name == user_in.name.lower()).first()

    if exists:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="El usuario ya existe")

    user = models.User(name=user_in.name.lower(), pass_hash = auth.password_hash(user_in.password), role = models.RoleEnum(user_in.role) if user_in.role in ("admin", "teacher", "student") else models.RoleEnum.student)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) :
    user = db.query(models.User).filter(models.User.name == form_data.username).first()
    
    if not user or not auth.verify_hash(form_data.password, user.pass_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nombre o contraseña incorrectas")
    
    token = auth.create_token({"sub": str(user.id), "name": user.name, "role": user.role})
    print(user.role)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead)
def me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.get("/admin")
def admin(_: models.User = Depends(auth.require_admin)):
    return{"status": True, "msg": "Credenciales de administrador"}