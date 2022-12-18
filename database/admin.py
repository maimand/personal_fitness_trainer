from typing import Union

from models.admin import Admin

admin_collection = Admin


async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


# todo: get user list


async def update_admin_data_with_email(email: str, data: dict) -> Union[bool, Admin]:
    user = await Admin.find_one({"email": email})
    if user:
        des_body = {k: v for k, v in data.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}
        await user.update(update_query)
        return user
    return False
