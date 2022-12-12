from typing import Optional

from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr


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


class AddAdminData(Document):
    fullname: str
    code: str
    email: Optional[str]
    phone: Optional[str]
    image: Optional[str]
    description: Optional[str]
    website: Optional[str]

    class Collection:
        name = "admin-code"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "123456",
                "phone": "123456",
                "image": "123456",
                "description": "123456",
                "website": "123456",
            }
        }
