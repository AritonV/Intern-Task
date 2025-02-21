from fastapi import FastAPI

from app.database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
  create_db_and_tables()


@app.get("/")
def home():
  return {"message": "Welcome to FastAPI CRUD App"}
