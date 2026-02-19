from fastapi import APIRouter
# from 

teacher_router = APIRouter(prefix="/teacher", tags=["teacher"])

@teacher_router.get("/")
async def home():
    return {"msg": "Welcome, teacher"}
