from fastapi import Body, APIRouter, HTTPException, Depends
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from auth.user import user_validate_token
from database.user import add_user, update_user_data
from models.super_admin import AddAdminData
from models.user import *
from auth.jwt_bearer import JWTBearer

router = APIRouter()
token_listener = JWTBearer()
hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    admin_exists = await User.find_one(User.email == user_credentials.username)
    if admin_exists:
        password = hash_helper.verify(
            user_credentials.password, admin_exists.password)
        if password:
            return sign_jwt(user_credentials.username)

        raise HTTPException(
            status_code=403,
            detail="Incorrect email or password"
        )

    raise HTTPException(
        status_code=403,
        detail="Incorrect email or password"
    )


@router.post("/new", response_model=UserData)
async def user_signup(user: User = Body(...)):
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=409,
            detail="User with email supplied already exists"
        )
    code_valid = await AddAdminData.find_one(AddAdminData.code == user.code)
    if code_valid:
        user.password = hash_helper.encrypt(user.password)
        new_admin = await add_user(user)
        return new_admin

    raise HTTPException(
        status_code=409,
        detail="User with code supplied not existed"
    )


@router.get("/get-info", response_model=DetailUserData, response_description='Get current user info')
async def get_user(user: User = Depends(user_validate_token)):
    return user


@router.put("/update", response_model=DetailUserData, response_description='Update current user info')
async def update_user(user: User = Depends(user_validate_token), req: UpdateUserModel = Body(...)):
    updated_user = await update_user_data(user, req.dict())
    return updated_user
