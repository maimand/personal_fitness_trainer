from datetime import datetime
from beanie import Document
from pydantic import BaseModel


class Food(BaseModel):
    id: str
    name: str
    ration: str
    calo: float
    protein: float
    fat: float
    carb: float
    fiber: float

    class Config:
        schema_extra = {
            "example": {
                "id": "com",
                "name": "Com trang",
                "ration": "1 chen vua",
                "calo": 200,
                "protein": 4.6,
                "fat": 0.6,
                "carb": 44.2,
                "fiber": 0.23
            }
        }


class FoodLog(Document):
    user: str
    foodId: str
    foodName: str
    time: datetime = datetime.now()
    number: int
    totalCaloriesIntake: int

    class Collection:
        name = "food-log"

    class Config:
        schema_extra = {
            "example": {
                "user": "man@mai.com",
                "foodId": "com-trang",
                "foodName": "Com trang",
                "time": datetime.now(),
                "number": 2,
                "totalCaloriesIntake": 300
            }
        }


class FoodLogBody(BaseModel):
    foodId: str
    foodName: str
    number: int
    totalCaloriesIntake: int

    class Config:
        schema_extra = {
            "example": {
                "foodId": "com-trang",
                "foodName": "com trang",
                "number": 2,
                "totalCaloriesIntake": 300
            }
        }
