from fastapi import HTTPException, Depends, status

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decode_jwt
from models.admin import Admin


async def admin_validate_token(jwtoken: str = Depends(JWTBearer())) -> Admin:
    payload = decode_jwt(jwtoken)
    user = await Admin.find_one({"email": payload["user_id"]})
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )
