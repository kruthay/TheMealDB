from fastapi import FastAPI
from app.routes.meals import router as meals_router

app = FastAPI()

app.include_router(meals_router, prefix="/api", tags=["meals"])

@app.get("/")
def read_root():
    return {"message": "Welcome to TheMealDB API"}
