from sqlalchemy import Column, Integer, String, Enum, DateTime, Float, Text, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .db import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class SubjectState(str, enum.Enum):
    ONGOING = "En proceso"
    FAILED = "Reprobado"
    PASSED = "Aprobado"

user_subject_association = Table(
    "usuarios_materias",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("materias.id", ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    pass_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.student, nullable=False)

    subjects = relationship(
        "Subject",
        secondary=user_subject_association,
        back_populates="users"
    )

class Subject(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(SubjectState), default=SubjectState.ONGOING, nullable=False)
    grade = Column(Float, default=0.0, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_timestamp = Column(DateTime(timezone=True), onupdate=func.now())

    users = relationship(
        "User",
        secondary=user_subject_association,
        back_populates="subjects"
    )
