from typing import List, Union

from beanie import PydanticObjectId

from models.admin import Admin
from models.student import Student
from models.super_admin import AddAdminData
from models.user import User

admin_collection = Admin
student_collection = Student
admins_collection = AddAdminData


async def add_admin(new_admin: Admin) -> Admin:
    admin = await new_admin.create()
    return admin


async def add_admin_code(new_admin: AddAdminData) -> AddAdminData:
    admin = await new_admin.create()
    return admin


async def retrieve_admin_code() -> List[AddAdminData]:
    codes = await admins_collection.all().to_list()
    return codes


async def retrieve_admins() -> List[Admin]:
    admins = await Admin.all().to_list()
    return admins


async def retrieve_users(admin: Admin) -> List[User]:
    users = await User.find_many({"code": admin.code}).to_list()
    return users


async def delete_admin_data(id: PydanticObjectId) -> bool:
    admin = await Admin.get(id)
    if admin:
        await admin.delete()
        return True


async def delete_user_data(email: str) -> bool:
    user = await User.find_one({"email": email})
    if user:
        await user.delete()
        return True


async def retrieve_students() -> List[Student]:
    students = await student_collection.all().to_list()
    return students


async def add_student(new_student: Student) -> Student:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> Student:
    student = await student_collection.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await student_collection.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in des_body.items()
    }}
    student = await student_collection.get(id)
    if student:
        await student.update(update_query)
        return student
    return False
