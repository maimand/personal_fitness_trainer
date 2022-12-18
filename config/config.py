from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from models.admin import Admin
from models.diet import FoodLog
from models.exercise import ExerciseLog
from models.student import Student
from models.super_admin import SuperAdmin, AddAdminData, Center
from models.user import User, UserLog


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: Optional[str] = "mongodb+srv://manmai:01694429810@cluster0.5bl5csu.mongodb.net/?retryWrites=true&w=majority"

    # JWT
    secret_key: str = "guiyfgc837tgf3iw87-012389764"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"
        orm_mode = True


async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(database=client['fitness'],
                      document_models=[Admin, Student, SuperAdmin, AddAdminData, Center, User, ExerciseLog, FoodLog, UserLog])
