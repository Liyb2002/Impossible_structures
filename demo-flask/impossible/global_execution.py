import copy
import random
import numpy as np
from . import procedural_objects
from . import LSystem
from . import write2JSON

import math
import json


def global_assign(procedural_objects_list, global_objects):
    for global_object in global_objects:
        action = global_object["action"]
        if action[0] == "assign":
            procedural_objects_list = action_assign(
                procedural_objects_list, global_object
            )
        if action[0] == "add":
            procedural_objects_list = action_add(procedural_objects_list, global_object)
        if action[0] == "add_multiple":
            procedural_objects_list = action_add_multiple(
                procedural_objects_list, global_object
            )
        if action[0] == "LSystem":
            procedural_objects_list += action_LSystem(
                procedural_objects_list, global_object
            )
        if action[0] == "matryoshka":
            procedural_objects_list += action_matryoshka(
                procedural_objects_list, global_object
            )

        # if action[0] == 'edit_size':
        #     procedural_objects_list += action_edit_size(procedural_objects_list, global_object)

    return procedural_objects_list


def action_assign(procedural_objects_list, global_object):
    for obj in procedural_objects_list:
        assign_available = False

        if obj.type == global_object["prev_type"]:
            assign_available = True
            for dir in obj.connected:
                for i in range(len(global_object["prev_condition"])):
                    prev_condition_dir = global_object["prev_condition"][i]
                    if dir == prev_condition_dir:
                        assign_available = False

        if assign_available:
            offset_x = random.uniform(
                global_object["offsets"][0][0], global_object["offsets"][0][1]
            )
            offset_y = random.uniform(
                global_object["offsets"][1][0], global_object["offsets"][1][1]
            )
            offset_z = random.uniform(
                global_object["offsets"][2][0], global_object["offsets"][2][1]
            )

            obj.position += np.array([offset_x, offset_y, offset_z])
            obj.length += np.array([offset_x, offset_y, offset_z])
            obj.type = global_object["object_id"]

    # for obj in procedural_objects_list:
    #     if obj.type == 6:
    #         print("broken")

    return procedural_objects_list


def action_add(procedural_objects_list, global_object):
    min_x, max_x, min_y, max_y, min_z, max_z = bounding_box(procedural_objects_list)

    dummy_scope = [0.1, 0.1]
    obj_xpos = 0.0
    obj_ypos = 0.0
    obj_zpos = 0.0
    obj_sizeX = 0.0
    obj_sizeY = 0.0
    obj_sizeZ = 0.0

    if global_object["size"][0][0] == "mult":
        obj_sizeX = (max_x - min_x) * global_object["size"][0][1]

    if global_object["size"][0][0] == "fixed":
        obj_sizeX = global_object["size"][0][1]

    if global_object["size"][1][0] == "fixed":
        obj_sizeY = global_object["size"][1][1]

    if global_object["size"][2][0] == "mult":
        obj_sizeZ = (max_z - min_z) * global_object["size"][2][1]

    if global_object["size"][2][0] == "fixed":
        obj_sizeZ = global_object["size"][2][1]

    if global_object["pos"][0][0] == "middle":
        obj_xpos = (min_x + max_x) / 2.0

    if global_object["pos"][0][0] == "positive":
        obj_xpos = max_x + global_object["pos"][0][1]

    if global_object["pos"][1][0] == "top":
        obj_ypos = max_y + global_object["pos"][1][1] + float(obj_sizeY)

    if global_object["pos"][1][0] == "bot":
        obj_ypos = min_y - global_object["pos"][1][1] - float(obj_sizeY)

    if global_object["pos"][1][0] == "positive":
        obj_ypos = max_y + global_object["pos"][1][1]

    if global_object["pos"][1][0] == "middle":
        obj_ypos = (min_y + max_y) / 2.0

    if global_object["pos"][2][0] == "middle":
        obj_zpos = (min_z + max_z) / 2.0

    if global_object["pos"][2][0] == "negative":
        obj_zpos = min_z - global_object["pos"][2][1]

    tempt_obj = procedural_objects.Procedural_object(
        global_object["object_id"],
        np.array([obj_xpos, obj_ypos, obj_zpos]),
        np.array([dummy_scope, dummy_scope, dummy_scope]),
        "00000",
        np.array([[0], [0], [0]]),
        np.array([0, 0, 0]),
    )
    tempt_obj.arbitrary_set_length(
        np.array([float(obj_sizeX), float(obj_sizeY), float(obj_sizeZ)])
    )
    procedural_objects_list.append(tempt_obj)
    return procedural_objects_list


def action_add_multiple(procedural_objects_list, global_object):
    target_count = len(procedural_objects_list)
    count = 0

    adding_types = global_object["adding_types"]
    for obj in procedural_objects_list:
        if obj.type not in adding_types:
            continue

        if count > target_count:
            break
        count += 1
        signs = random_sign(3)
        offsets = random_number(3)
        pos = obj.position
        length = obj.length

        new_obj_scopeX = np.array(
            [global_object["scope_x"][0], global_object["scope_x"][1]]
        )
        new_obj_scopeY = np.array(
            [global_object["scope_y"][0], global_object["scope_y"][1]]
        )
        new_obj_scopeZ = np.array(
            [global_object["scope_z"][0], global_object["scope_z"][1]]
        )
        new_obj_rotationX = random.choice(global_object["rotation"][0])
        new_obj_rotationY = random.choice(global_object["rotation"][1])
        new_obj_rotationZ = random.choice(global_object["rotation"][2])

        new_obj_pos = (
            obj.position
            + np.array(
                [
                    signs[0] * obj.length[0],
                    signs[1] * offsets[1] * obj.length[1],
                    signs[2] * offsets[2] * obj.length[2],
                ]
            )
            + np.array(
                [
                    signs[0] * new_obj_scopeX[0],
                    signs[1] * new_obj_scopeY[0],
                    signs[2] * new_obj_scopeZ[0],
                ]
            )
        )
        tempt_obj = procedural_objects.Procedural_object(
            9,
            new_obj_pos,
            np.array([new_obj_scopeX, new_obj_scopeY, new_obj_scopeZ]),
            "00000",
            np.array([[new_obj_rotationX], [new_obj_rotationY], [new_obj_rotationZ]]),
            np.array([0, 0, 0]),
        )
        procedural_objects_list.append(tempt_obj)

    return procedural_objects_list


def action_LSystem(procedural_objects_list, global_object):
    min_x, max_x, min_y, max_y, min_z, max_z = bounding_box(procedural_objects_list)
    center = np.array([(min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2])
    group_count = 1
    result = []
    system_data = []
    light_pos = np.array([0, 0, 0])
    for obj in procedural_objects_list:
        if obj.type == global_object["light_type"]:
            light_pos = obj.position
            break

    for obj in procedural_objects_list:
        dist_to_light = math.sqrt(
            (obj.position[0] - light_pos[0]) ** 2
            + (obj.position[1] - light_pos[1]) ** 2
            + (obj.position[2] - light_pos[2]) ** 2
        )
        base_prob = 1.0
        prob = max(base_prob - (0.15 * dist_to_light), 0.1)

        if obj.type in global_object["adding_types"] and random.random() < prob:
            line2 = light_pos - obj.position
            rotation_x, rotation_y, rotation_z = rotation_matrix(line2)
            rotation_x += round(random.uniform(-0.2, 0.2), 4)
            rotation_y += round(random.uniform(-0.2, 0.2), 4)
            rotation_z += round(random.uniform(-0.2, 0.2), 4)

            system = LSystem.LSys()
            system.system_setup(
                obj.position,
                np.array([rotation_x, rotation_y, rotation_z]),
                group_count,
                light_pos,
            )
            system.run_system()
            result += system.finish_system()

            data = {
                "System": {
                    "group": group_count,
                    "origin_x": float(obj.position[0]),
                    "origin_y": float(obj.position[1]),
                    "origin_z": float(obj.position[2]),
                    "system_rotation_x": float(rotation_x),
                    "system_rotation_y": float(rotation_y),
                    "system_rotation_z": float(rotation_z),
                }
            }
            system_data.append(data)

            group_count += 1

    with open("three/system.json", "w") as f:
        json.dump(system_data, f, indent=2)

    return result


def action_edit_size(procedural_objects_list, global_object):
    for obj in procedural_objects_list:
        if obj.type in global_object["prev_type"]:
            len_x = obj.length[0]
            len_y = obj.length[1]
            len_z = obj.length[2]

            if (
                global_object["condition"][0] == "smaller"
                and len_x < global_object["condition"][1]
                and len_y < global_object["condition"][1]
                and len_z < global_object["condition"][1]
            ):
                edit_index = max_of_three(obj.length[0], obj.length[1], obj.length[2])
                obj.length[edit_index] = global_object["target"]

    return procedural_objects_list


def action_matryoshka(procedural_objects_list, global_object):
    output_writer = write2JSON.output()
    inner_matryoshka = []

    for obj in procedural_objects_list:
        if (
            obj.type == global_object["prev_type"]
            and random.random() < global_object["prob"]
        ):
            inner_matryoshka.append(obj)
            obj.type = global_object["object_id"]

    output_writer.write_proceudral_objects(inner_matryoshka, "./inner_layer.json")

    return []


def random_sign(number):
    signs = []
    for i in range(0, number):
        rand_num = random.random()
        if rand_num > 0.5:
            signs.append(1)
        else:
            signs.append(-1)

    return signs


def random_number(number):
    rand_offsets = []
    for i in range(0, number):
        rand_num = random.random()
        rand_offsets.append(rand_num * 0.5)

    return rand_offsets


def bounding_box(procedural_objects_list):
    min_x = 100
    max_x = -100
    min_y = 100
    max_y = -100
    min_z = 100
    max_z = -100

    for obj in procedural_objects_list:
        if min_x > obj.position[0] - obj.length[0]:
            min_x = obj.position[0] - obj.length[0]
        if max_x < obj.position[0] + obj.length[0]:
            max_x = obj.position[0] + obj.length[0]

        if min_y > obj.position[1] - obj.length[1]:
            min_y = obj.position[1] - obj.length[1]
        if max_y < obj.position[1] + obj.length[1]:
            max_y = obj.position[1] + obj.length[1]

        if min_z > obj.position[2] - obj.length[2]:
            min_z = obj.position[2] - obj.length[2]
        if max_z < obj.position[2] + obj.length[2]:
            max_z = obj.position[2] + obj.length[2]

    return (min_x, max_x, min_y, max_y, min_z, max_z)


def max_of_three(a, b, c):
    if a > b and a > c:
        return 0

    if b > a and b > c:
        return 1

    return 2


def rotation_matrix(target_vector):
    source = np.array([1, 0, 0])
    target = np.asarray(target_vector)

    source = source / np.linalg.norm(source)  # Normalize source vector
    target = target / np.linalg.norm(target)  # Normalize target vector

    v = np.cross(source, target)  # Cross product of source and target
    c = np.dot(source, target)  # Dot product of source and target

    skew_symmetric = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

    rotation = (
        np.eye(3)
        + skew_symmetric
        + np.dot(skew_symmetric, skew_symmetric) * (1 / (1 + c))
    )
    x, y, z = rotation_matrix_to_euler_angles(rotation)
    return x, y, z


def rotation_matrix_to_euler_angles(rotation_matrix):
    sy = np.sqrt(
        rotation_matrix[0, 0] * rotation_matrix[0, 0]
        + rotation_matrix[1, 0] * rotation_matrix[1, 0]
    )
    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        y = np.arctan2(-rotation_matrix[2, 0], sy)
        z = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    else:
        x = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        y = np.arctan2(-rotation_matrix[2, 0], sy)
        z = 0

    return x, y, z
