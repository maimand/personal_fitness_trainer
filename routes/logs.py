from beanie import PydanticObjectId
from database.logs import add_exercise_log_to_db, retrieve_exercise_log, delete_exercise_log_from_db, \
    add_food_log_to_db, retrieve_food_log, delete_food_log_from_db, retrieve_user_log
from database.user import add_user_log
from models.diet import FoodLogBody, FoodLog
from models.exercise import ExerciseLogBody, ExerciseLog
from models.student import Response
from fastapi import Body, APIRouter, Depends
from auth.user import user_validate_token
from models.user import *

router = APIRouter()


@router.get("/exercises-logs", response_description="Exercise logs retrieved", response_model=Response)
async def get_exercises_logs(user: User = Depends(user_validate_token)):
    logs = await retrieve_exercise_log(user.email)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": logs
    }


@router.get("/food-logs", response_description="Food logs retrieved", response_model=Response)
async def get_food_logs(user: User = Depends(user_validate_token)):
    logs = await retrieve_food_log(user.email)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Food logs data retrieved successfully",
        "data": logs
    }


@router.get("/body-logs", response_description="Body logs retrieved", response_model=Response)
async def get_body_logs(user: User = Depends(user_validate_token)):
    logs = await retrieve_user_log(user.email)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Body logs data retrieved successfully",
        "data": logs
    }


@router.post("/food-logs", response_description="Food logs added into the database", response_model=Response)
async def add_food_log(user1: User = Depends(user_validate_token), body: FoodLogBody = Body(...)):
    food_log = FoodLog(user=user1.email, foodId=body.foodId, foodName=body.foodName, time=datetime.now(timezone.utc),
                       number=body.number, totalCaloriesIntake=body.totalCaloriesIntake)
    new_log = await add_food_log_to_db(food_log)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Student created successfully",
        "data": new_log
    }


@router.post("/body-logs", response_description="Body logs added into the database", response_model=Response)
async def add_body_log(user1: User = Depends(user_validate_token), body: UserLogBody = Body(...)):
    body_log = UserLog(user=user1.email, image=body.image, time=datetime.now(timezone.utc))
    new_log = await add_user_log(body_log)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Student created successfully",
        "data": new_log
    }


@router.delete("/food/{id}", response_description="Food log data deleted from the database",
               dependencies=[Depends(user_validate_token)])
async def delete_food_log(id: PydanticObjectId):
    deleted_log = await delete_food_log_from_db(id)
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


@router.post("/exercises-logs", response_description="Exercise logs added into the database", response_model=Response)
async def add_exercise_log(user1: User = Depends(user_validate_token), body: ExerciseLogBody = Body(...)):
    exercise_log = ExerciseLog(user=user1.email, exerciseName=body.exerciseName, time=datetime.now(timezone.utc),
                               reps=body.reps, totalCaloriesBurn=body.totalCaloriesBurn)
    new_log = await add_exercise_log_to_db(exercise_log)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Student created successfully",
        "data": new_log
    }


@router.delete("/exercise/{id}", response_description="Student data deleted from the database",
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



