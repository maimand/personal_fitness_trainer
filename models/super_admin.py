from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


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
                "username": "abdul@youngest.dev",
                "password": "3xt3m#"
            }
        }


class AddAdminData(Document):
    fullname: str
    code: str

    class Collection:
        name = "admin-code"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "code": "123456",
            }
        }
