from fastapi import HTTPException, Depends, status

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decode_jwt
from models.super_admin import SuperAdmin


async def super_admin_validate_token(jwtoken: str = Depends(JWTBearer())) -> SuperAdmin:
    payload = decode_jwt(jwtoken)
    user = await SuperAdmin.find_one({"email": payload["user_id"]})
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )
