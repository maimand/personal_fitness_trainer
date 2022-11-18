from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from database.database import add_admin, add_admin_code
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


@router.post("/add-admin", response_model=AddAdminData)
async def admin_signup(admin_name):
    admin = AddAdminData(fullname=admin_name, code=hash_helper.encrypt(admin_name))
    new_admin = await add_admin_code(admin)
    return new_admin
