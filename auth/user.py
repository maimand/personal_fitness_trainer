from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decode_jwt
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def user_validate_token(jwtoken: str = Depends(JWTBearer())) -> User:
    payload = decode_jwt(jwtoken)
    user = await User.find_one({"email": payload["user_id"]})
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )
