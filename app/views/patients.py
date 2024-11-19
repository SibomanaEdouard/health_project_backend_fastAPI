from uuid import UUID
from fastapi import APIRouter, Depends
from app.controllers.patient_controller import get_patients, create_patient,update_patient,delete_patient,get_patient
from app.models.patient import PatientCreate,PatientUpdate

router = APIRouter()

# this is the endpoint to get all patients 
@router.get("/patients")
async def list_patients():
    return await get_patients()

# this is the endpoint to  create new patient 
@router.post("/patients")
async def add_patient(patient: PatientCreate):
    return await create_patient(patient)

from fastapi import Path
from uuid import UUID

@router.put("/patients/{id}")
async def update_patient_view(patient: PatientUpdate, id: str = Path(..., title="The ID of the patient")):
    # Trim leading/trailing spaces from the ID
    id = id.strip()
    # Validate the ID after trimming
    try:
        id = UUID(id)
    except ValueError as e:
        return {"message": f"Invalid UUID: {str(e)}"}
    return await update_patient(patient, id)



@router.delete("/patients/{id}")
async def delete_patient_view(id: str = Path(..., title="The ID of the patient")):
        # Trim leading/trailing spaces from the ID
    id = id.strip()
    # Validate the ID after trimming
    try:
        id = UUID(id)
    except ValueError as e:
        return {"message": f"Invalid UUID: {str(e)}"}
    return await delete_patient(id)


@router.get("/patients/{id}")
async def get_patient_view(id):
        # Trim leading/trailing spaces from the ID
    id = id.strip()
    # Validate the ID after trimming
    try:
        id = UUID(id)
    except ValueError as e:
        return {"message": f"Invalid UUID: {str(e)}"}
    return await get_patient(id)
