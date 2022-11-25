import asyncio
from typing import List, Union

import requests

from models.exercise import Exercise, ExerciseDetail

url = "https://exerciseapi3.p.rapidapi.com/search/"

headers = {
    "X-RapidAPI-Key": "bbf11e7827msh68b8edc80e10e74p1b9755jsn257ce29150ec",
    "X-RapidAPI-Host": "exerciseapi3.p.rapidapi.com"
}

detail_url = "https://exercises-by-api-ninjas.p.rapidapi.com/v1/exercises"

detail_headers = {
    "X-RapidAPI-Key": "bbf11e7827msh68b8edc80e10e74p1b9755jsn257ce29150ec",
    "X-RapidAPI-Host": "exercises-by-api-ninjas.p.rapidapi.com"
}


def map_exercise(res):
    name = res['Name']
    video_url = res['Youtube link']
    exercise = Exercise(name=name, videoUrl=video_url)
    return exercise


def map_exercise_detail(res):
    calories_burn = 100
    name = ''
    difficulty = res['difficulty']
    instructions = res['instructions']
    if difficulty == 'beginner':
        calories_burn = 100
    if difficulty == 'intermediate':
        calories_burn = 150
    if difficulty == 'expert':
        calories_burn = 200
    video_url = ''
    exercise = ExerciseDetail(name=name, videoUrl=video_url,
                              difficulty=difficulty, instructions=instructions, caloriesBurn=calories_burn)
    return exercise


async def get_exercises_by_body_part_request(name) -> List[Exercise]:
    if name != '':
        querystring = {"primaryMuscle": name}
    else:
        querystring = {"primaryMuscle": "pectoralis major"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = map(map_exercise, response.json())
    if res:
        return list(res)
    else:
        return []


async def get_exercises_by_name_request(name) -> List[Exercise]:
    querystring = {"name": name}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = map(map_exercise, response.json())
    if res:
        return list(res)
    else:
        return []


async def get_exercise_detail_request(name) -> List[ExerciseDetail]:
    querystring = {"name": name}
    response = requests.request("GET", detail_url, headers=detail_headers, params=querystring)
    res = map(map_exercise_detail, response.json())
    if res:
        return list(res)
    else:
        return []


async def get_exercise_detail(name) -> Union[bool, ExerciseDetail]:
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
            return c
    return False
