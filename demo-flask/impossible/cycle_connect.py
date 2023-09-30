from . import produce
import numpy as np
import random


def Available_Ending_With_Object(generic_object_list, target_obj):
    possible_endings = []
    for i in range(1, len(generic_object_list)):
        for connect_id in generic_object_list[int(i)].connect_id:
            if connect_id == target_obj.type:
                possible_endings.append(i)

    return possible_endings


def Available_Ending_With_Direction(generic_object_list, direction):
    possible_endings = []
    for i in range(1, len(generic_object_list)):
        if generic_object_list[i].able_next_direction(direction):
            possible_endings.append(i)

    return possible_endings


def get_dirs(delta):
    directions = []
    if delta[0] > 0:
        directions.append("+x")
    if delta[0] <= 0:
        directions.append("-x")
    if delta[1] > 0:
        directions.append("+y")
    if delta[1] <= 0:
        directions.append("-y")
    if delta[2] > 0:
        directions.append("+z")
    if delta[2] <= 0:
        directions.append("-z")

    return directions


def update_order(objStart, directions):
    if objStart.arriving_rule == "+x" or objStart.arriving_rule == "-x":
        tempt_dir = directions[0]
        directions[0] = directions[1]
        directions[1] = tempt_dir

    return directions


def random_order():
    orders = []
    first = random.randint(0, 1)
    second = (first + 1) % 2
    third = 2

    orders.append(first)
    orders.append(second)
    orders.append(third)
    return orders
