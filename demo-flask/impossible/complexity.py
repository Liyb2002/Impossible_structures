import random


def calc_complexity(visual_bridge_info):
    # print(visual_bridge_info)

    if visual_bridge_info["complexity"] == 0:
        visual_bridge_info["foreground_index"] = (
            visual_bridge_info["foreground_index"] * 4.0
        )
        visual_bridge_info["background_index"] = (
            visual_bridge_info["background_index"] * 4.0
        )
        visual_bridge_info["steps"] = int(visual_bridge_info["steps"] / 3)
        # print("user defined steps and distance")
        return visual_bridge_info

    c = visual_bridge_info["complexity"]
    foreground_index = 2.0 + random.random()
    d = dist_by_level(c) + random.random()
    background_index = foreground_index + d
    s = int((c * c + 10 - 2 * d * d) / 2)
    s = max(1, s)

    visual_bridge_info["foreground_index"] = foreground_index * 4
    visual_bridge_info["background_index"] = background_index * 4
    visual_bridge_info["steps"] = int(s / 3)

    return visual_bridge_info


def dist_by_level(c):
    if c < 4.0:
        return 2.0
    if c < 8.0:
        return 3.0

    return 4.0
