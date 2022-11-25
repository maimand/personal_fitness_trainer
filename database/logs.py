from typing import List

from beanie import PydanticObjectId

from models.exercise import ExerciseLog
from models.user import User


async def retrieve_exercise_log(user: User) -> List[ExerciseLog]:
    logs = await ExerciseLog.find_many({"user": user.email}).to_list()
    return logs


async def add_exercise_log_to_db(log: ExerciseLog) -> ExerciseLog:
    exercise_log = await log.create()
    return exercise_log


async def delete_exercise_log_from_db(id: PydanticObjectId) -> bool:
    log = await ExerciseLog.get(id)
    if log:
        await log.delete()
        return True
