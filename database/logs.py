from typing import List

from beanie import PydanticObjectId

from models.diet import FoodLog
from models.exercise import ExerciseLog
from models.user import User, UserLog


async def retrieve_exercise_log(user: str) -> List[ExerciseLog]:
    logs = await ExerciseLog.find_many({"user": user}).to_list()
    return logs


async def add_exercise_log_to_db(log: ExerciseLog) -> ExerciseLog:
    exercise_log = await log.create()
    return exercise_log


async def delete_exercise_log_from_db(id: PydanticObjectId) -> bool:
    log = await ExerciseLog.get(id)
    if log:
        await log.delete()
        return True


async def retrieve_food_log(user: str) -> List[FoodLog]:
    logs = await FoodLog.find_many({"user": user}).to_list()
    return logs


async def retrieve_user_log(user: str) -> List[UserLog]:
    logs = await UserLog.find_many({"user": user}).to_list()
    return logs


async def add_food_log_to_db(log: FoodLog) -> FoodLog:
    food_log = await log.create()
    return food_log


async def delete_food_log_from_db(id: PydanticObjectId) -> bool:
    log = await FoodLog.get(id)
    if log:
        await log.delete()
        return True
