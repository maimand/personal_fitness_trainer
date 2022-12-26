from fastapi import APIRouter

from models.diet import Food
from models.student import Response
from services.diet import get_all_food_data, get_food_data
from fastapi_pagination import Page, paginate

router = APIRouter()


@router.get("/", response_description="All food retrieved", response_model=Page[Food])
async def get_all_food(food: str = ''):
    try:
        res = get_all_food_data(food)
        r = paginate(res)
        return r
    except:
        res = get_all_food_data('com')
        r = paginate(res)
        return r


@router.get("/{name}", response_description="Exercise retrieved", response_model=Response)
async def get_food(name: str = ''):
    res = get_food_data(name)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Exercises data retrieved successfully",
        "data": res
    }

# todo: predict food via image
