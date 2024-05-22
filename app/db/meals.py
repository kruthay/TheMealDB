from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
from app.models import MealModel

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.themealdb

async def get_meals(category: Optional[str], area: Optional[str], tags: Optional[List[str]]) -> List[MealModel]:
    query = {}
    if category:
        query["category"] = category
    if area:
        query["area"] = area
    if tags:
        query["tags"] = {"$all": tags}

    meals = await db["meals"].find(query).to_list(100)
    return meals

async def get_meal(meal_id: str) -> Optional[MealModel]:
    meal = await db["meals"].find_one({"_id": ObjectId(meal_id)})
    return meal

async def get_meal_by_name(name: str) -> Optional[MealModel]:
    meal = await db["meals"].find_one({"name": name})
    return meal

async def create_meal(meal: MealModel) -> MealModel:
    result = await db["meals"].insert_one(meal.dict(by_alias=True))
    meal.id = result.inserted_id
    return meal

async def update_meal(meal_id: str, meal: MealModel) -> Optional[MealModel]:
    update_result = await db["meals"].update_one({"_id": ObjectId(meal_id)}, {"$set": meal.dict(by_alias=True)})
    if update_result.modified_count == 1:
        updated_meal = await db["meals"].find_one({"_id": ObjectId(meal_id)})
        return updated_meal
    return None

async def delete_meal(meal_id: str) -> bool:
    delete_result = await db["meals"].delete_one({"_id": ObjectId(meal_id)})
    return delete_result.deleted_count == 1
