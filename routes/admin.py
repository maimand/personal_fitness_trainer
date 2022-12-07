from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from auth.admin import admin_validate_token
from auth.jwt_handler import sign_jwt
from database.database import add_admin, retrieve_users, delete_user_data
from database.logs import retrieve_exercise_log, retrieve_food_log
from models.admin import Admin, AdminData, AdminSignIn
from models.student import Response

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == admin_credentials.username)
    if admin_exists:
        password = hash_helper.verify(
            admin_credentials.password, admin_exists.password)
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


@router.post("/new", response_model=AdminData)
async def admin_signup(admin: Admin = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == admin.email)
    if admin_exists:
        raise HTTPException(
            status_code=409,
            detail="Admin with email supplied already exists"
        )

    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(admin)
    return new_admin


@router.delete("/delete/{email}", response_description="User deleted from the database",
               dependencies=[Depends(admin_validate_token)])
async def delete_user(email: str):
    deleted_log = await delete_user_data(email)
    if deleted_log:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "User with ID: {} removed".format(id),
            "data": deleted_log
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Log with id {0} doesn't exist".format(id),
        "data": False
    }


@router.get("/exercises-logs/{email}", response_description="Exercise logs retrieved", response_model=Response,
            dependencies=[Depends(admin_validate_token)])
async def get_exercises_logs(email: str):
    logs = await retrieve_exercise_log(email)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": logs
    }


@router.get("/food-logs/{email}", response_description="Food logs retrieved", response_model=Response,
            dependencies=[Depends(admin_validate_token)])
async def get_food_logs(email: str):
    logs = await retrieve_food_log(email)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": logs
    }


@router.get("/get-users", response_description="Users data retrieved", response_model=Response)
async def get_users(admin: Admin = Depends(admin_validate_token)):
    admins = await retrieve_users(admin)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": admins
    }


@router.get("/get-code", response_description="Code data retrieved", response_model=Response)
async def get_code(admin: Admin = Depends(admin_validate_token)):
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Code data retrieved successfully",
        "data": admin
    }
