from typing import Optional, List

from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr, BaseModel


class SuperAdmin(Document):
    email: EmailStr
    password: str

    class Collection:
        name = "super-admin"

    class Config:
        schema_extra = {
            "example": {
                "email": "abdul@youngest.dev",
                "password": "3xt3m#",
            }
        }


class SuperAdminSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "superadmin@test.com",
                "password": "123456"
            }
        }


class Center(Document):
    fullname: str
    code: str
    email: Optional[str]
    phone: Optional[str]
    image: Optional[str]
    description: Optional[str]
    website: Optional[str]

    class Collection:
        name = "center"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "123456",
                "phone": "123456",
                "code": "123456",
                "image": "123456",
                "description": "123456",
                "website": "123456",
            }
        }


class AddAdminRequest(BaseModel):
    center: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "center": "123456",
                "email": "man@gmail.com",
            }
        }


class AddAdminData(Document):
    email: EmailStr
    code: str
    center: str

    class Collection:
        name = "center-admin"

    class Config:
        schema_extra = {
            "example": {
                "code": "123456",
                "email": "man@gmail.com",
            }
        }
