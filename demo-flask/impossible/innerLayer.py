import json
from . import generate
from . import perspective
from . import read_file

from copy import deepcopy
import numpy as np


def produce_innerLayer(matryoshka_path, decorate_path):
    (
        visual_bridge_info,
        new_generic_object_list,
        global__object_list,
        extra_system_list,
    ) = read_file.read_object_file(matryoshka_path)

    multipler = 0.4
    result_list = []
    camera = perspective.ortho_camera()

    for new_generic_object in new_generic_object_list:
        new_generic_object.adjust_scope(multipler)

    with open("inner_layer.json", "r") as object_file:
        objects_data = json.load(object_file)

        for object_data in objects_data:
            center_x = object_data["obj"]["start_x"]
            center_y = object_data["obj"]["start_y"]
            center_z = object_data["obj"]["start_z"]

            scope_x = object_data["obj"]["scale_x"]
            scope_y = object_data["obj"]["scale_y"]
            scope_z = object_data["obj"]["scale_z"]

            foreground_intersection = np.array(
                [center_x + 0.4, center_y + 0.4, center_z + 0.4]
            )
            background_intersection = camera.get_intersections_withPos(
                foreground_intersection, 6
            )

            visual_bridge_info["foreground_index"] = 12
            visual_bridge_info["background_index"] = 20
            visual_bridge_info["steps"] = 1
            visual_bridge_info["startPos"] = [400, 400]

            class_generate = generate.generate_helper(
                new_generic_object_list,
                global__object_list,
                extra_system_list,
                visual_bridge_info,
                decorate_path,
            )
            result_list += class_generate.smc_process(
                foreground_intersection, background_intersection
            )[0]

    for obj in result_list:
        obj.type = int(obj.type) + 100

    return result_list
