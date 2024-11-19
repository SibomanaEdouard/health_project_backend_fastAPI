from fastapi import FastAPI
from app.database import engine, Base
from app.views import patients, appointments, billing

# Initialize database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# FastAPI app
app = FastAPI(on_startup=[init_db])

# Routers
app.include_router(patients.router, prefix="/api/v1")
# app.include_router(appointments.router, prefix="/api")
# app.include_router(billing.router, prefix="/api")
@app.get("/")
async def welcome():
    return {"message": "Welcome to the fastapi project"}
