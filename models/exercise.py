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
