from typing import Optional
import uuid
from sqlalchemy import UUID, Column, Integer, String
from app.database import Base
from pydantic import BaseModel, ConfigDict


class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)
    age = Column(Integer)
    address = Column(String)
    medicine = Column(String)
    email = Column(String,unique=True) 

class PatientBase(BaseModel):
    name: str
    age: int
    address: str
    medicine:str
    email:str

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: uuid.UUID

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    medicine: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True
