import json
from . import generic_objects


def read_object_file(file_path):
    generic_object_list = []
    global__object_list = []
    extra_system_list = []

    visual_bridge_info = None

    with open(file_path, "r") as object_file:
        objects_data = json.load(object_file)

        if "lhs_type" in objects_data[0]:
            return (
                visual_bridge_info,
                generic_object_list,
                global__object_list,
                extra_system_list,
            )

        generic_object_list.append(generic_objects.Generic_object(objects_data[1]))
        for object_data in objects_data:
            if object_data["object_id"] == -1:
                visual_bridge_info = object_data
            if object_data["object_id"] > 0:
                if object_data["type"] == "local_object":
                    new_object = generic_objects.Generic_object(object_data)
                    generic_object_list.append(new_object)
                if object_data["type"] == "global_object":
                    global__object_list.append(object_data)
                if object_data["type"] == "extra_system":
                    extra_system_list.append(object_data)
                    new_object = generic_objects.Generic_object(object_data)
                    generic_object_list.append(new_object)

    return (
        visual_bridge_info,
        generic_object_list,
        global__object_list,
        extra_system_list,
    )
