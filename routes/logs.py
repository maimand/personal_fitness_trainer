from beanie import PydanticObjectId
from database.logs import add_exercise_log_to_db, retrieve_exercise_log, delete_exercise_log_from_db
from models.exercise import ExerciseLogBody, ExerciseLog
from models.student import Response
from fastapi import Body, APIRouter, Depends
from auth.user import user_validate_token
from models.user import *

router = APIRouter()


@router.get("/exercises-logs", response_description="Exercise logs retrieved", response_model=Response)
async def get_exercises_logs(user: User = Depends(user_validate_token)):
    logs = await retrieve_exercise_log(user)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": logs
    }


@router.get("/food-logs", response_description="Food logs retrieved", response_model=Response)
async def get_food_logs(name: str):
    return


@router.post("/exercises-logs", response_description="Food logs added into the database", response_model=Response)
async def add_exercise_log(user1: User = Depends(user_validate_token), body: ExerciseLogBody = Body(...)):
    exercise_log = ExerciseLog(user=user1.email, exerciseName=body.exerciseName,
                               reps=body.reps, totalCaloriesBurn=body.totalCaloriesBurn)
    new_log = await add_exercise_log_to_db(exercise_log)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Student created successfully",
        "data": new_log
    }


@router.delete("/{id}", response_description="Student data deleted from the database",
               dependencies=[Depends(user_validate_token)])
async def delete_exercise_log(id: PydanticObjectId):
    deleted_log = await delete_exercise_log_from_db(id)
    if deleted_log:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Log with ID: {} removed".format(id),
            "data": deleted_log
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Log with id {0} doesn't exist".format(id),
        "data": False
    }
