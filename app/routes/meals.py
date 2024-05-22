from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas import MealCreate, MealUpdate, Meal
from app.db import meals as db_meals
from app.models import MealModel

router = APIRouter()

@router.get("/meals", response_model=List[MealModel])
async def read_meals(
    category: Optional[str] = Query(None, description="Filter by category"),
    area: Optional[str] = Query(None, description="Filter by area"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags")
):
    meals = await db_meals.get_meals(category, area, tags)
    return meals

@router.get("/meals/{meal_id}", response_model=MealModel)
async def read_meal(meal_id: str):
    meal = await db_meals.get_meal(meal_id)
    if meal:
        return meal
    raise HTTPException(status_code=404, detail="Meal not found")

@router.post("/meals", response_model=MealModel)
async def create_meal(meal: MealCreate):
    existing_meal = await db_meals.get_meal_by_name(meal.name)
    if existing_meal:
        raise HTTPException(status_code=400, detail="Meal with this name already exists")

    meal_model = MealModel(**meal.dict())
    created_meal = await db_meals.create_meal(meal_model)
    
    return created_meal

@router.put("/meals/{meal_id}", response_model=MealModel)
async def update_meal(meal_id: str, meal: MealUpdate):
    meal_model = MealModel(**meal.dict())
    updated_meal = await db_meals.update_meal(meal_id, meal_model)
    if updated_meal:
        return updated_meal
    raise HTTPException(status_code=404, detail="Meal not found")

@router.delete("/meals/{meal_id}", response_model=dict)
async def delete_meal(meal_id: str):
    if await db_meals.delete_meal(meal_id):
        return {"message": "Meal deleted"}
    raise HTTPException(status_code=404, detail="Meal not found")
