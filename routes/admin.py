from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from auth.admin import admin_validate_token
from auth.jwt_handler import admin_sign_jwt
from database.database import add_admin, delete_user_data
from database.logs import retrieve_exercise_log, retrieve_food_log
from database.user import update_user_data_with_email
from models.admin import Admin, AdminData, AdminSignIn
from models.student import Response
from models.super_admin import AddAdminData, Center
from models.user import User
from services.mail import send_enable_email, send_disable_email

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn = Body(...)):
    admin_exists = await Admin.find_one(Admin.email == admin_credentials.username)
    if admin_exists:
        if not admin_exists.active:
            raise HTTPException(
                status_code=403,
                detail="Admin is being disabled"
            )
        password = hash_helper.verify(
            admin_credentials.password, admin_exists.password)
        if password:
            return admin_sign_jwt(admin_credentials.username)

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
    admin_exist = await Admin.find_one(Admin.email == admin.email)
    if admin_exist:
        raise HTTPException(
            status_code=409,
            detail="Admin with email supplied already existed"
        )
    code_valid = await AddAdminData.find_one(AddAdminData.code == admin.code)
    if code_valid:
        admin.password = hash_helper.encrypt(admin.password)
        admin.center = code_valid.center
        admin.active = True
        new_admin = await add_admin(admin)
        return new_admin
    raise HTTPException(
        status_code=409,
        detail="Code supplied not valid"
    )


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


@router.get("/disable/{email}", response_description="User deleted from the database",
            dependencies=[Depends(admin_validate_token)])
async def disable_user(email: str):
    res = await update_user_data_with_email(email, {'active': False})
    send_disable_email(email)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User with email: {} disabled".format(email),
        "data": res
    }


@router.get("/enable/{email}", response_description="User deleted from the database",
            dependencies=[Depends(admin_validate_token)])
async def enable_user(email: str):
    res = await update_user_data_with_email(email, {'active': True})
    send_enable_email(email)

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "User with email: {} enabled".format(email),
        "data": res
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
    users = await User.find_many({"code": admin.center, 'request': False}).to_list()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Users data retrieved successfully",
        "data": users
    }


@router.get("/get-request-users", response_description="Users data retrieved", response_model=Response)
async def get_request_users(admin: Admin = Depends(admin_validate_token)):
    users = await User.find_many({"code": admin.center, 'request': True}).to_list()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Inactive users retrieved successfully",
        "data": users
    }


@router.get("/get-code", response_description="Code data retrieved", response_model=Response)
async def get_code(admin: Admin = Depends(admin_validate_token)):
    center = await  Center.find_one({'code': admin.center})
    admin.centerName = center.fullname
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Code data retrieved successfully",
        "data": admin
    }


@router.get("/reset-password/{email}", response_description="Code data retrieved", response_model=Response,
            dependencies=[Depends(admin_validate_token)])
async def reset_password(email: str):
    res = await update_user_data_with_email(email, {'password': hash_helper.encrypt('000000')})
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Code data retrieved successfully",
        "data": res
    }


@router.get("/accept/{email}", response_description="Code data retrieved", response_model=Response,
            dependencies=[Depends(admin_validate_token)])
async def accept_user(email: str):
    res = await update_user_data_with_email(email, {'request': False, 'active': True})
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Code data retrieved successfully",
        "data": res
    }
