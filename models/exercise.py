from datetime import datetime, timezone
from beanie import Document
from pydantic import BaseModel


class Exercise(BaseModel):
    name: str
    videoUrl: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Barbell Bench Press",
                "videoUrl": "https://www.youtube.com/watch?v=rT7DgCr-3pg&t=29s&ab_channel=ScottHermanFitness",
            }
        }


class ExerciseDetail(BaseModel):
    name: str
    videoUrl: str
    difficulty: str
    instructions: str
    caloriesBurn: float

    class Config:
        schema_extra = {
            "example": {
                "name": "Barbell Bench Press",
                "videoUrl": "https://www.youtube.com/watch?v=rT7DgCr-3pg&t=29s&ab_channel=ScottHermanFitness",
                "difficulty": "intermediate",
                "instructions": "Barbell Bench Press",
                "caloriesBurn": 150.0
            }
        }


class ExerciseLog(Document):
    user: str
    exerciseName: str
    time: datetime = datetime.now(timezone.utc)
    reps: int
    totalCaloriesBurn: int

    class Collection:
        name = "exercise-log"

    class Config:
        schema_extra = {
            "example": {
                "user": "man@mai.com",
                "exerciseName": "Push up",
                "time": datetime.now(),
                "reps": 10,
                "totalCaloriesBurn": 1000
            }
        }


class ExerciseLogBody(BaseModel):
    exerciseName: str
    reps: int
    totalCaloriesBurn: int

    class Config:
        schema_extra = {
            "example": {
                "exerciseName": "Push up",
                "reps": 10,
                "totalCaloriesBurn": 1000
            }
        }
