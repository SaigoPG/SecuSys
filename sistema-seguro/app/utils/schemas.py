from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    password: str = Field(min_length=8, max_length=25)
    role: Literal["teacher", "student"]


class UserRead(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    name: str
    role: str


class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = "En proceso"
    grade: Optional[float] = 0.0


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    grade: Optional[float] = None
    status: Optional[str] = None


class SubjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    grade: float
    timestamp: datetime
    update_timestamp: Optional[datetime]

    class Config:
        from_attributes = True



class SubjectWithUsers(SubjectRead):
    users: List[UserRead] = []


class UserWithSubjects(UserRead):
    subjects: List[SubjectRead] = []