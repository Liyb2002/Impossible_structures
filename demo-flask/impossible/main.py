from . import write2JSON
from . import generate
from . import innerLayer
from . import read_file
from . import initLSystem
from . import complexity

MIN_C = 0
MAX_C = 7


def run(file_path, decorate_path, c: 0, matryoshka_path=None):
    if c < MIN_C or c > MAX_C:
        return {"Error": "invalid complexity parameter"}

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
    visual_bridge_info["complexity"] = c

    if visual_bridge_info is None:
        print("L-System backbone")
        result_list = initLSystem.initSystem(decorate_path)
    else:
        visual_bridge_info = complexity.calc_complexity(visual_bridge_info)
        class_generate = generate.generate_helper(
            generic_object_list,
            global__object_list,
            extra_system_list,
            visual_bridge_info,
            decorate_path,
        )
        result_list, intersections = class_generate.smc_process()

        print("impossible structure success!")
    if matryoshka_path:
        result_list += innerLayer.produce_innerLayer(matryoshka_path, decorate_path)

    print("success!")
    output_writer = write2JSON.output()
    return output_writer.write_result(result_list, intersections)
