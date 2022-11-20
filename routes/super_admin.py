from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from auth.super_admin import super_admin_validate_token
from database.database import *
from models.student import Response
from models.super_admin import SuperAdmin, SuperAdminSignIn, AddAdminData

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def super_admin_login(admin_credentials: SuperAdminSignIn = Body(...)):
    admin_exists = await SuperAdmin.find_one(SuperAdmin.email == admin_credentials.username)
    if admin_exists:
        # login for super admin is temp
        password = admin_credentials.password == admin_exists.password
        if password:
            return sign_jwt(admin_credentials.username)

        raise HTTPException(
            status_code=403,
            detail="Incorrect email or password"
        )

    raise HTTPException(
        status_code=403,
        detail="Incorrect email or password"
    )


@router.post("/add-admin", response_model=AddAdminData, dependencies=[Depends(super_admin_validate_token)])
async def add_admin(admin_name: str = Body(...)):
    admin = AddAdminData(fullname=admin_name, code=hash_helper.encrypt(admin_name))
    new_admin = await add_admin_code(admin)
    return new_admin


@router.post("/get-admin-codes", response_description="Admin data retrieved", response_model=Response,
             dependencies=[Depends(super_admin_validate_token)])
async def get_admins():
    admins = await retrieve_admin_code()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": admins
    }
