from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    fullname: str
    email: EmailStr
    password: str
    code: str

    class Collection:
        name = "user"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
                "password": "3xt3m#",
                "code": "123456",
            }
        }


class UserToken(Document):
    userId: str
    access_token: str

    class Collection:
        name = "user-token"

    class Config:
        schema_extra = {
            "example": {
                "userId": "Abdulazeez Abdulazeez Adeshina",
                "access_token": "123456abc"
            }
        }


class UserSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {
                "username": "abdul@youngest.dev",
                "password": "3xt3m#"
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

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdul@youngest.dev",
            }
        }
