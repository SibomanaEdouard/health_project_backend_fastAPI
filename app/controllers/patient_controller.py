import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.exc import NoResultFound
from app.models.patient import Patient, PatientCreate, PatientUpdate
from app.database import async_session
from uuid import UUID


async def get_patients():
    async with async_session() as session:
        result = await session.execute(select(Patient))
        return result.scalars().all()


# this is the logic to register the patient in the system 
async def create_patient(patient_data: PatientCreate):
    async with async_session() as session:
        try:
            # Validate required fields
            if not all([patient_data.address, patient_data.age, patient_data.email, patient_data.name]):
                return {"message": "All details are required to register the patient"}
            
            # Check if the email already exists
            query = select(Patient).where(Patient.email == patient_data.email)
            result = await session.execute(query)
            existing_patient = result.scalar()
            
            if existing_patient:
                return {"message": "The email you are trying to register already exists in the system"}
            
            # Create a new patient instance
            new_patient = Patient(**patient_data.dict())
            
            # Add and commit to the database
            session.add(new_patient)
            await session.commit()
            
            # Return success message
            return {"patient": new_patient, "message": "Patient created successfully!"}
        
        except Exception as e:
            # Handle any exception and rollback if needed
            await session.rollback()
            return {"message": f"An error occurred: {str(e)}"}




async def update_patient(patient_data: PatientUpdate, id: uuid.UUID):
    async with async_session() as session:
        try:
            # Find patient by ID
            result = await session.execute(select(Patient).where(Patient.id == id))
            existing_patient = result.scalar_one_or_none()

            if not existing_patient:
                return {"message": "No patient with the specified ID in the system"}

            # Update fields
            for key, value in patient_data.dict(exclude_unset=True).items():
                setattr(existing_patient, key, value)

            # Add and commit the updated patient
            session.add(existing_patient)
            await session.commit()

            # Return success response
            return {
                "patient": existing_patient,
                "message": "The patient was updated successfully"
            }

        except Exception as e:
            # Rollback on error
            await session.rollback()
            return {"message": f"Internal server error .... : {str(e)}"}



async def delete_patient(id: uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(Patient).where(Patient.id == id))
        patient = result.scalar_one_or_none()

        if not patient:
            return {"message": "No patient found with the specified identity"}

        await session.execute(delete(Patient).where(Patient.id == id))
        await session.commit()

        return {"message": "The patient was deleted successfully"}

async def get_patient(id:uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(Patient).where(Patient.id == id))
        patient =result.scalar_one_or_none()
        if not patient:
            return{"message":"No patient retrieved with the specified Identity"}

        return ({"patient":patient},{"message":"The patient retrieved successfully"})    
