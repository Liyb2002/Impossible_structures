from . import LSystem
import numpy as np
from . import decorations
import json
from . import write2JSON
import copy


def initSystem(decorate_path):
    print("hello")

    start_pos = np.array([0, 0, 0])
    rotation = np.array([0, 0, 0])
    group_count = 1
    light_pos = np.array([5, 5, 5])

    system = LSystem.LSys()
    system.system_setup(
        start_pos,
        rotation,
        group_count,
        light_pos,
        sys_path="multiTree/backbone.json",
        init_size=np.array([0.2, 2.0, 0.2]),
    )
    system.run_system()
    L_backbone = system.finish_system()

    output_writer = write2JSON.output()

    # inner_matryoshka = []
    # for obj in L_backbone:
    #     if obj.type == 13:
    #         inner_matryoshka.append(obj)

    # inner_matryoshka = reduceDuplicate.reduce(inner_matryoshka)[:2]

    inner_matryoshka = find_mid_point(L_backbone)
    output_writer.write_proceudral_objects(inner_matryoshka, "./inner_layer.json")

    decorator = decorations.decoration_operator(decorate_path)
    decoration_list = decorator.decorate(L_backbone)
    write_group(start_pos, rotation)

    return decoration_list


def write_group(start_pos, rotation):
    system_data = []
    data = {
        "System": {
            "group": 1,
            "origin_x": float(start_pos[0]),
            "origin_y": float(start_pos[1]),
            "origin_z": float(start_pos[2]),
            "system_rotation_x": float(rotation[0]),
            "system_rotation_y": float(rotation[1]),
            "system_rotation_z": float(rotation[2]),
        }
    }
    system_data.append(data)

    with open("three/system.json", "w") as f:
        json.dump(system_data, f, indent=2)


def find_mid_point(L_backbone):
    x_mid, y_mid, z_mid, count = 0, 0, 0, 0
    for obj in L_backbone:
        count += 1.0
        x_mid += obj.position[0]
        y_mid += obj.position[1]
        z_mid += obj.position[2]

    x_mid = x_mid / count + 5.0
    y_mid = y_mid / count + 2.0
    z_mid = z_mid / count

    obj = copy.deepcopy(L_backbone[0])
    obj.position = np.array([x_mid, y_mid, z_mid])

    inner_matryoshka = []
    inner_matryoshka.append(obj)

    # obj2 = copy.deepcopy(L_backbone[0])
    # obj2.position = np.array([x_mid-7.0, y_mid-5.0, z_mid-3.0])
    # inner_matryoshka.append(obj2)

    return inner_matryoshka
