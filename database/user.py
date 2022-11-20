from typing import Union

from models.user import User, UserToken

user_collection = User


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user


async def add_user_token(new_user: UserToken) -> UserToken:
    user = await new_user.create()
    return user


async def update_user_data(user: User, data: dict) -> Union[bool, User]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    await user.update(update_query)
    return user
