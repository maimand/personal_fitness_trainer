from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from auth.jwt_handler import admin_sign_jwt
from auth.super_admin import super_admin_validate_token
from database.admin import update_admin_data_with_email
from database.database import *
from models.student import Response
from models.super_admin import SuperAdmin, SuperAdminSignIn, AddAdminData, Center, AddAdminRequest
from services.gen_code import gen_code
from services.mail import *

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def super_admin_login(admin_credentials: SuperAdminSignIn = Body(...)):
    try:
        admin_exists = await SuperAdmin.find_one(SuperAdmin.email == admin_credentials.username)
        if admin_exists:
            # login for super admin is temp
            password = admin_credentials.password == admin_exists.password
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
    except Exception as e:
        return {'error': str(e)}


@router.post("/add-admin", response_model=AddAdminData, dependencies=[Depends(super_admin_validate_token)])
async def add_admin_to_center(request: AddAdminRequest):
    name_existed = await AddAdminData.find_one({'center': request.center, 'email': request.email})
    if name_existed:
        raise HTTPException(
            status_code=404,
            detail="Email is already existed"
        )
    code = gen_code()
    send_email(request.email, code)
    new_admin_request = AddAdminData(email=request.email, code=code, center=request.center)
    new_request = await new_admin_request.create()
    return new_request


@router.post("/add-center", response_model=Center, dependencies=[Depends(super_admin_validate_token)])
async def add_center(center: Center):
    name_existed = await Center.find_one(Center.email == center.email)
    if name_existed:
        raise HTTPException(
            status_code=404,
            detail="Center is already existed"
        )
    new_center = await center.create()
    return new_center


@router.delete("/delete/{id}", response_description="Admin hard deleted from the database"
    , dependencies=[Depends(super_admin_validate_token)])
async def delete_admin(id: PydanticObjectId):
    deleted_log = await delete_admin_data(id)
    if deleted_log:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Admin with ID: {} removed".format(id),
            "data": deleted_log
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Log with id {0} doesn't exist".format(id),
        "data": False
    }


@router.get("/get-admins", response_description="Admin data retrieved", response_model=Response,
            dependencies=[Depends(super_admin_validate_token)])
async def get_admins():
    admins = await retrieve_admins()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": admins
    }


@router.get("/disable-admin/{admin}", response_description="Admin data retrieved", response_model=Response,
            dependencies=[Depends(super_admin_validate_token)])
async def disable_admin(admin: str):
    admins = await update_admin_data_with_email(admin, {'active': False})
    send_disable_email(admin)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": admins
    }


@router.get("/enable-admin/{admin}", response_description="Admin data retrieved", response_model=Response,
            dependencies=[Depends(super_admin_validate_token)])
async def disable_admin(admin: str):
    admins = await update_admin_data_with_email(admin, {'active': True})
    send_enable_email(admin)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": admins
    }


@router.get("/get-admin-codes/{center}", response_description="Admin data retrieved", response_model=Response,
            dependencies=[Depends(super_admin_validate_token)])
async def get_admin_codes(center: str):
    emails = await AddAdminData.find_many({"center": center}).to_list()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": emails
    }


@router.get("/get-center", response_description="Admin data retrieved", response_model=Response,
            dependencies=[Depends(super_admin_validate_token)])
async def get_admin_codes():
    emails = await Center.all().to_list()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Students data retrieved successfully",
        "data": emails
    }
