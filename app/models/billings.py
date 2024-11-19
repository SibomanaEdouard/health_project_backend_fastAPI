from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    amount = Column(Float)
    description = Column(String)

# Pydantic schema
from pydantic import BaseModel

class BillingBase(BaseModel):
    patient_id: int
    amount: float
    description: str

class BillingCreate(BillingBase):
    pass

class BillingResponse(BillingBase):
    id: int

    class Config:
        orm_mode = True
