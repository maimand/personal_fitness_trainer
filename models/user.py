from datetime import datetime, timezone

from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional


class User(Document):
    fullname: str
    email: EmailStr
    password: str
    code: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    fatPercent: Optional[float]
    fullname: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    active: bool = False
    request: bool = True

    class Collection:
        name = "user"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "password": "3xt3m#",
                "code": "123456",
                "height": 1.7,
                "weight": 70.0,
                "fatPercent": 20.0,
                "age": 23,
                "gender": "male"
            }
        }


class UserSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "man@amai.com",
                "password": "123456"
            }
        }


class UserData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
            }
        }


class DetailUserData(BaseModel):
    fullname: str
    email: EmailStr
    height: Optional[float]
    weight: Optional[float]
    fatPercent: Optional[float]
    fullname: Optional[str]
    age: Optional[int]
    gender: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "height": 1.7,
                "weight": 70.0,
                "fatPercent": 70.0,
                "age": 23,
                "gender": "male"
            }
        }


class UpdateUserModel(BaseModel):
    height: Optional[float]
    weight: Optional[float]
    fatPercent: Optional[float]
    fullname: Optional[str]
    age: Optional[int]
    gender: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez",
                "height": 1.7,
                "weight": 70.0,
                "fatPercent": 70.0,
                "age": 23,
                "gender": "male"
            }
        }


class UpdateUserPasswordModel(BaseModel):
    oldPassword: Optional[str]
    newPassword: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "oldPassword": "Abdulazeez Abdulazeez",
                "newPassword": "male"
            }
        }


class UserLog(Document):
    user: str
    image: str
    time: datetime = datetime.now(timezone.utc)

    class Collection:
        name = "user-log"

    class Config:
        schema_extra = {
            "example": {
                "user": "man@mai.com",
                "image": "",
                "time": datetime.now(),
            }
        }


class UserLogBody(BaseModel):
    image: str
    time: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "image": "",
            }
        }
