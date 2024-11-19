from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(String)
    reason = Column(String)

# Pydantic schema
from pydantic import BaseModel

class AppointmentBase(BaseModel):
    patient_id: int
    date: str
    reason: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
