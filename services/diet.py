from typing import List
import pandas as pd
from models.diet import Food


def get_food_data(food) -> Food:
    df = pd.read_csv('/Users/pcomssb/PycharmProjects/personal_fitness_trainer/services/normalized_data.csv')
    selected_row = df.loc[df['Normalized'].str.contains(food)]
    if not selected_row.empty:
        return Food(
            id=food,
            name=selected_row.values[0][0],
            ration=selected_row.values[0][1],
            calo=selected_row.values[0][2],
            protein=selected_row.values[0][3],
            fat=selected_row.values[0][4],
            carb=selected_row.values[0][5],
            fiber=selected_row.values[0][6],
        )


def map_list_to_food(input_list) -> Food:
    return Food(
        id=input_list[7], name=input_list[0],
        ration=input_list[1],
        calo=input_list[2],
        protein=input_list[3],
        fat=input_list[4],
        carb=input_list[5],
        fiber=input_list[6],
    )


def get_all_food_data(food) -> List[Food]:
    df = pd.read_csv('/Users/pcomssb/PycharmProjects/personal_fitness_trainer/services/normalized_data.csv')
    if food:
        foods = df.loc[df['Normalized'].str.contains(food)].values.tolist()
    else:
        foods = df.values.tolist()
    food_list = list(map(lambda a: map_list_to_food(a), foods))
    if food_list:
        return food_list
