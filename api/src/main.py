# To run localhost execute: uvicorn main:app --app-dir src --reload

from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()


from routes.mutant_routes import mutant_router
from routes.teacher_routes import teacher_router

app.include_router(mutant_router)
app.include_router(teacher_router)
