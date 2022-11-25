import asyncio
from fastapi import APIRouter
from models.student import Response
from services.exercises import *

router = APIRouter()


@router.get("/", response_description="Exercise retrieved", response_model=Response)
async def get_exercises(name: str = ''):
    res = await get_exercises_by_body_part_request(name)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Exercises data retrieved successfully",
        "data": res
    }


@router.get("/{name}", response_description="Exercise detail data retrieved", response_model=Response)
async def get_exercise_detail(name: str):
    a, b = await asyncio.gather(
        get_exercises_by_name_request(name),
        get_exercise_detail_request(name)
    )
    if a:
        ex = a[0]
        if b:
            c = b[0]
            c.name = ex.name
            c.videoUrl = ex.videoUrl
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "Exercise detail return",
                "data": c
            }
        else:
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "Exercise detail return",
                "data": ex
            }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Exercise doesn't exist",
    }

# @router.post("/", response_description="Student data added into the database", response_model=Response)
# async def add_student_data(student: Student = Body(...)):
#     new_student = await add_student(student)
#     return {
#         "status_code": 200,
#         "response_type": "success",
#         "description": "Student created successfully",
#         "data": new_student
#     }
#
#
# @router.delete("/{id}", response_description="Student data deleted from the database")
# async def delete_student_data(id: PydanticObjectId):
#     deleted_student = await delete_student(id)
#     if deleted_student:
#         return {
#             "status_code": 200,
#             "response_type": "success",
#             "description": "Student with ID: {} removed".format(id),
#             "data": deleted_student
#         }
#     return {
#         "status_code": 404,
#         "response_type": "error",
#         "description": "Student with id {0} doesn't exist".format(id),
#         "data": False
#     }
#
#
# @router.put("{id}", response_model=Response)
# async def update_student(id: PydanticObjectId, req: UpdateStudentModel = Body(...)):
#     updated_student = await update_student_data(id, req.dict())
#     if updated_student:
#         return {
#             "status_code": 200,
#             "response_type": "success",
#             "description": "Student with ID: {} updated".format(id),
#             "data": updated_student
#         }
#     return {
#         "status_code": 404,
#         "response_type": "error",
#         "description": "An error occurred. Student with ID: {} not found".format(id),
#         "data": False
#     }
