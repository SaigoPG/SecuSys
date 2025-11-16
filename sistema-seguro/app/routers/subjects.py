from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.utils import models, schemas, auth
from app.utils.db import get_db

router = APIRouter(prefix="/subjects",tags=["materias"])

@router.post("/", response_model=schemas.SubjectRead, status_code=status.HTTP_201_CREATED)
def add_subject(subject_in: schemas.SubjectCreate, db: Session = Depends(get_db), _: models.User = Depends(auth.require_admin)):

    new_subject = models.Subject(name = subject_in.name, description = subject_in.description)

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

@router.get("/", response_model = list[schemas.SubjectRead])
def get_subjects(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):

    if current_user.role == models.RoleEnum.student:
        return db.query(models.Subject).filter(models.Subject.user_id == current_user.id).all()
    
    return db.query(models.Subject).all()

@router.put("/{subject_id}/grade", response_model = schemas.SubjectRead)
def update_grade(subject_id: int, subject_in: schemas.SubjectUpdate, db: Session = Depends(get_db), _:models.User = Depends(auth.require_teacher)):

    subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Materia no encontrada")
    
    if subject_in.grade is not None:
        subject.grade = subject_in.grade

    db.commit()
    db.refresh(subject)
    return subject

@router.delete("/{subject_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db), _: models.User = Depends(auth.require_admin)):

    subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Materia no encontrada")
    
    db.delete(subject)
    db.commit()