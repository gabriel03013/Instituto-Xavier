# To run localhost execute: uvicorn main:app --app-dir src --reload

from fastapi import FastAPI
from dotenv import load_dotenv

app = FastAPI()

from routes.admin_routes import admin_router
from routes.mutante_routes import mutante_router
from routes.professor_routes import professor_router

app.include_router(admin_router)
app.include_router(mutante_router)
app.include_router(professor_router)