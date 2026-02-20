from fastapi import APIRouter

professor_router = APIRouter(prefix="/professor", tags=["professor"])

@professor_router.get("/")
async def home():
    return {"msg": "Welcome, professor"}
