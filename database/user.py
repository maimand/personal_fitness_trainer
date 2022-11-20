from models.user import User, UserToken

user_collection = User


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user


async def add_user_token(new_user: UserToken) -> UserToken:
    user = await new_user.create()
    return user
