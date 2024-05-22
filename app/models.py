from pydantic import BaseModel
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class MealModel(BaseModel):
    id: PyObjectId = None
    name: str
    category: str
    area: str
    instructions: str
    tags: list[str] = []

    class Config:
        json_encoders = {
            ObjectId: str,
        }
