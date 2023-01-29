import numpy as np

import intersection
import particle

PI = 3.14159265
DEFAULT_CONFIG = {
    "num_connections": 1,
    "num_particles": 300,
    "beam_mean": 6,
    "beam_sd": 2,
    "block_size": 0.05,
    "X_freedom": False,
    "Y_freedom": False,
    "input_structure": [],
}


def generate(layers, intersections):
    config = DEFAULT_CONFIG
    config["layer_index"] = []
    config["intersection_pos"] = []
    config["connection"] = []
    config["num_blocks_per_layer"] = []

    for i, ixn in enumerate(intersections):
        l1 = ixn["layer1"]
        l2 = ixn["layer2"]
        x = round(ixn["u"] * 800)
        y = round(ixn["v"] * 800)

        config["layer_index"].append(layers[l1]["z"])
        config["layer_index"].append(layers[l2]["z"])
        config["num_blocks_per_layer"].append(layers[l1]["num_blocks"])
        config["num_blocks_per_layer"].append(layers[l2]["num_blocks"])
        config["intersection_pos"].append([x, y])
        config["connection"].append([2 * i + 1, 2 * i + 2])

        if i < len(intersections) - 1:
            config["connection"].append([2 * i + 2, 2 * i + 3])

    num_intersection = len(config["intersection_pos"])
    max_score = -1000
    result_particle = None
    intersections = []

    foreground_index = int(config["layer_index"][0])
    background_index = int(config["layer_index"][1])
    basic_scene = intersection.Scene([400, 400])

    startPos = np.array(
        [config["intersection_pos"][0][0], config["intersection_pos"][0][1]]
    )
    dforeground_intersection = basic_scene.get_possible_intersects(foreground_index)
    dbackground_intersection = basic_scene.get_possible_intersects(background_index)
    portion = background_index / foreground_index

    foreground_intersection = basic_scene.get_intersection_t(
        startPos, dforeground_intersection
    )
    background_intersection = basic_scene.get_intersection_t(
        startPos, dbackground_intersection
    )

    intersections.append(foreground_intersection)
    intersections.append(background_intersection)

    extra_foreground_index = []
    extra_background_index = []
    extra_foreground_intersection = []
    extra_background_intersection = []
    extra_backPortion = []

    for i in range(1, num_intersection):
        e_foreground_index = int(config["layer_index"][2 * i])
        e_background_index = int(config["layer_index"][2 * i + 1])
        dforeground_intersection = basic_scene.get_possible_intersects(
            e_foreground_index
        )
        dbackground_intersection = basic_scene.get_possible_intersects(
            e_background_index
        )
        e_startPos = np.array(
            [config["intersection_pos"][i][0], config["intersection_pos"][i][1]]
        )
        e_foreground_intersection = basic_scene.get_intersection_t(
            e_startPos, dforeground_intersection
        )
        e_background_intersection = basic_scene.get_intersection_t(
            e_startPos, dbackground_intersection
        )
        back_portion = e_background_index / e_foreground_index
        extra_foreground_index.append(e_foreground_index)
        extra_background_index.append(e_background_index)
        extra_foreground_intersection.append(e_foreground_intersection)
        extra_background_intersection.append(e_background_intersection)
        intersections.append(e_foreground_intersection)
        intersections.append(e_background_intersection)
        extra_backPortion.append(back_portion)

    particle_list = []
    score_list = []
    # initialize particles
    for i in range(config["num_particles"]):
        tempt_particle = particle.Particle(
            foreground_index,
            background_index,
            foreground_intersection,
            background_intersection,
            portion,
            config["num_connections"],
            config["block_size"],
            config["Y_freedom"],
        )
        tempt_particle.generate_structures()

        for j in range(num_intersection - 1):
            tempt_particle.set_intersections(
                extra_foreground_index[j],
                extra_background_index[j],
                extra_foreground_intersection[j],
                extra_background_intersection[j],
                1.0,
                extra_backPortion[j],
            )

        tempt_particle.get_connecting_comp(config["connection"])
        tempt_score = tempt_particle.total_score()
        particle_list.append(tempt_particle)
        score_list.append(tempt_score)

    particle_list = particle.resample(particle_list, score_list)

    for i in range(num_intersection * 2):
        layer = 2 * num_intersection - i
        blocks = config["num_blocks_per_layer"][layer - 1]

        cc = 0
        for i in config["connection"]:
            if i[0] == layer or i[1] == layer:
                cc += 1

        extra_block = max(0, blocks - cc * config["beam_mean"])
        steps = int(extra_block / config["beam_mean"])
        for s in range(steps):
            score_list = []
            for i in range(len(particle_list)):
                particle_list[i].structures[layer].generate(
                    1, config["beam_mean"], config["beam_sd"]
                )
                score_list.append(particle_list[i].total_score())

            particle_list = particle.resample(particle_list, score_list)

    # finish the process
    for s in range(2):
        for i in range(len(particle_list)):
            particle_list[i].finish(s)
            score_list[i] = particle_list[i].total_score()

        particle_list = particle.resample(particle_list, score_list)
        result_particle = particle_list[0]

    # Write the result
    result = []
    for cc in result_particle.connecting_comp:
        i = cc.get_object()
        data = {
            "type": "beam",
            "obj": {
                "start_x": i.start_x,
                "start_y": i.start_y,
                "start_z": i.start_z,
                "scale_x": i.scale_x,
                "scale_y": i.scale_y,
                "scale_z": i.scale_z,
            },
        }
        result.append(data)

    for structure in result_particle.structures:
        for i in structure.rect:
            data = {
                "type": "beam",
                "layer": structure.layer,
                "obj": {
                    "start_x": i.start_x,
                    "start_y": i.start_y,
                    "start_z": i.start_z,
                    "scale_x": i.scale_x,
                    "scale_y": i.scale_y,
                    "scale_z": i.scale_z,
                },
            }
            result.append(data)

    return result
