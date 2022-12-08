from typing import Optional

from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class Admin(Document):
    fullname: str
    email: EmailStr
    password: str
    code: str
    center: Optional[str]

    class Collection:
        name = "admin"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "password": "3xt3m#",
                "center": "cali",
                "code": "123456"
            }
        }


class AdminSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "danang@cali.com",
                "password": "123456"
            }
        }


class AdminData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
            }
        }
