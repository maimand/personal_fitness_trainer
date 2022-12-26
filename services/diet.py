from typing import List
import pandas as pd
from models.diet import Food
from difflib import SequenceMatcher

df = pd.read_csv('services/normalized_data.csv')
df = df.fillna(0)


def get_food_data(food) -> Food:
    for ind in df.index:
        if SequenceMatcher(None, df['Normalized'][ind], food).ratio() > 0.8:
            selected_row = df.iloc[[ind]]
            res = map_list_to_food(selected_row.values[0])
            # res = Food(
            #     id=food,
            #     name=selected_row.values[0][0],
            #     ration=selected_row.values[0][1],
            #     calo=selected_row.values[0][2],
            #     protein=selected_row.values[0][3],
            #     fat=selected_row.values[0][4],
            #     carb=selected_row.values[0][5],
            #     fiber=selected_row.values[0][6],
            #     image=selected_row.values[0][8],
            # )
            return res
    # if not selected_row:
    #     res = Food(
    #         id=food,
    #         name=selected_row[0].values[0][0],
    #         ration=selected_row[0].values[0][1],
    #         calo=selected_row[0].values[0][2],
    #         protein=selected_row[0].values[0][3],
    #         fat=selected_row[0].values[0][4],
    #         carb=selected_row[0].values[0][5],
    #         fiber=selected_row[0].values[0][6],
    #         image=selected_row[0].values[0][8],
    #     )
    #     return res


def map_list_to_food(input_list) -> Food:
    return Food(
        id=input_list[7], name=input_list[0],
        ration=input_list[1],
        calo=float(input_list[2]),
        protein=float(input_list[3]),
        fat=float(input_list[4]),
        carb=float(input_list[5]),
        fiber=float(input_list[6]),
        image=input_list[8],
    )


def get_all_food_data(food) -> List[Food]:
    foods = []
    if food:
        for ind in df.index:
            if SequenceMatcher(None, df['Normalized'][ind], food).ratio() > 0.4:
                selected_row = df.iloc[[ind]]
                foods.append(selected_row.values[0])
    else:
        foods = df.values.tolist()
    food_list = list(map(lambda a: map_list_to_food(a), foods))
    if food_list:
        return food_list
    else:
        return []

