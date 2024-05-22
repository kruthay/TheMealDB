from pydantic import BaseModel, Field
from typing import List, Optional

class MealBase(BaseModel):
    name: str
    category: str
    area: str
    instructions: str
    tags: Optional[List[str]] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Spaghetti Carbonara",
                "category": "Pasta",
                "area": "Italian",
                "instructions": "Boil pasta. Fry pancetta. Mix with eggs and cheese.",
                "tags": ["pasta", "Italian"]
            }
        }

class MealCreate(MealBase):
    pass

class MealUpdate(MealBase):
    pass

class Meal(MealBase):
    id: str = Field(..., alias='_id')

