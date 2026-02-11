# To run localhost execute: uvicorn main:app --app-dir src --reload

from fastapi import Depends, FastAPI
from dotenv import load_dotenv

app = FastAPI()


from routes.mutant_routes import mutant_router
from routes.teacher_routes import teacher_router

app.include_router(mutant_router)
app.include_router(teacher_router)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Authentication Demo"}

@app.get("/protected")
async def protected_route(current_user: str = Depends(authenticate_user)):
    return {"message": f"Hello {current_user}, this is a protected route!"}