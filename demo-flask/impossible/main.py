from . import write2JSON
from . import generate
from . import innerLayer
from . import read_file
from . import initLSystem
from . import complexity


FILE_MAP = {
    "za": "impossible/ZA_Extended/ZA_monumentValley.json",
    "mt": "impossible/matryoshka/matryoshka.json",
    "tr": "impossible/tree/tree.json",
}

DECORATE_MAP = {
    "za": "impossible/ZA_Extended/ZA_monumentValley_decorate.json",
    "mt": "impossible/matryoshka/matryoshka_decorate.json",
    "tr": "impossible/tree/tree_decorate.json",
}

MT_PATH = "impossible/matryoshka/matryoshka_inner.json"


def run(args):
    scene = args["scene"]
    file_path = FILE_MAP[scene]
    decorate_path = DECORATE_MAP[scene]

    # read the inputs
    generic_object_list = []
    global__object_list = []
    extra_system_list = []
    result_list = []

    (
        visual_bridge_info,
        generic_object_list,
        global__object_list,
        extra_system_list,
    ) = read_file.read_object_file(file_path)

    if visual_bridge_info is None:
        # print("L-System backbone")
        result_list = initLSystem.initSystem(decorate_path)
    else:
        # print("DEFAULT")
        # print(visual_bridge_info)

        visual_bridge_info["startPos"] = [
            float(args["startPos_x"]),
            float(args["startPos_y"]),
        ]
        visual_bridge_info["foreground_index"] = float(args["foreground_index"])
        visual_bridge_info["background_index"] = float(args["background_index"])
        visual_bridge_info["num_visual_bridge"] = int(args["num_visual_bridge"])
        visual_bridge_info["steps"] = int(args["steps"])

        # print("CUSTOM")
        # print(visual_bridge_info)

        visual_bridge_info = complexity.calc_complexity(visual_bridge_info)
        class_generate = generate.generate_helper(
            generic_object_list,
            global__object_list,
            extra_system_list,
            visual_bridge_info,
            decorate_path,
        )
        result_list, intersections = class_generate.smc_process()

        # print("impossible structure success!")
    if scene == "mt":
        result_list += innerLayer.produce_innerLayer(MT_PATH, decorate_path)

    # print("success!")
    output_writer = write2JSON.output()
    return output_writer.write_result(result_list, intersections)


# def run(file_path, decorate_path, matryoshka_path=None):
#     # read the inputs
#     generic_object_list = []
#     global__object_list = []
#     extra_system_list = []
#     result_list = []

#     (
#         visual_bridge_info,
#         generic_object_list,
#         global__object_list,
#         extra_system_list,
#     ) = read_file.read_object_file(file_path)

#     if visual_bridge_info is None:
#         # print("L-System backbone")
#         result_list = initLSystem.initSystem(decorate_path)
#     else:
#         visual_bridge_info = complexity.calc_complexity(visual_bridge_info)
#         class_generate = generate.generate_helper(
#             generic_object_list,
#             global__object_list,
#             extra_system_list,
#             visual_bridge_info,
#             decorate_path,
#         )
#         result_list, intersections = class_generate.smc_process()

#         # print("impossible structure success!")
#     if matryoshka_path:
#         result_list += innerLayer.produce_innerLayer(matryoshka_path, decorate_path)

#     # print("success!")
#     output_writer = write2JSON.output()
#     return output_writer.write_result(result_list, intersections)
