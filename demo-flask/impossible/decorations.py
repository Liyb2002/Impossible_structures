import json
import numpy as np
from . import procedural_objects
import random


class decoration_operator:
    def __init__(self, decorate_path):
        self.generic_footprint_list = []
        self.generic_nonterminal_list = []
        self.generic_terminal_list = []
        self.decorate_path = decorate_path

        self.read_decorations()

    def read_decorations(self):
        with open(self.decorate_path, "r") as object_file:
            objects_data = json.load(object_file)

            new_object = generic_footprint_object(objects_data[0])
            self.generic_footprint_list.append(new_object)

            for object_data in objects_data:
                if object_data["category"] == "footprint":
                    new_object = generic_footprint_object(object_data)
                    self.generic_footprint_list.append(new_object)

                if object_data["category"] == "nonterminal":
                    new_object = generic_nonterminal_object(object_data)
                    self.generic_nonterminal_list.append(new_object)

                if object_data["category"] == "terminal":
                    new_object = generic_terminal_object(object_data)
                    self.generic_terminal_list.append(new_object)

    def decorate(self, procedural_objects):
        # go through all main objects produced
        instance_list = []

        for obj in procedural_objects:
            input_type = obj.type
            min_pos = obj.position - obj.length
            max_pos = obj.position + obj.length
            rotation = obj.rotation
            group = obj.group

            # if we have decoration for this main object
            for footprint_object in self.generic_footprint_list:
                if footprint_object.structural_id == input_type:
                    # get a random subdivison rule
                    subdiv_rule = footprint_object.execute_subdiv()

                    # execute the subdivision rule
                    total_nonterminal_list, total_terminal_list = self.parse_rule(
                        subdiv_rule, min_pos, max_pos, rotation, group
                    )

                    while len(total_nonterminal_list) > 0:
                        nonterminal_obj = total_nonterminal_list[-1]
                        total_nonterminal_list.pop()

                        generic_nonterminal_object = self.generic_nonterminal_list[
                            int(nonterminal_obj.type)
                        ]
                        subdiv_rule = generic_nonterminal_object.execute_subdiv()
                        tempt_nonterminal_list, tempt_terminal_list = self.parse_rule(
                            subdiv_rule,
                            nonterminal_obj.min_pos,
                            nonterminal_obj.max_pos,
                            rotation,
                            group,
                        )

                        total_terminal_list += tempt_terminal_list
                        total_nonterminal_list += tempt_nonterminal_list
                    instance_list += total_terminal_list

        return instance_list

    def parse_rule(self, subdiv_rule, min_pos, max_pos, rotation, group):
        split_dir = subdiv_rule[1]
        scope = max_pos - min_pos
        culmulative_percentage = 0

        nonterminal_list = []
        terminal_list = []

        for i in range(2, len(subdiv_rule)):
            new_obj_info = subdiv_rule[i]

            if split_dir == "x direction":
                tempt_min_pos = min_pos + np.array(
                    [culmulative_percentage * scope[0], 0, 0]
                )
                culmulative_percentage += new_obj_info[2]
                tempt_max_pos = np.array(
                    [
                        min_pos[0] + culmulative_percentage * scope[0],
                        max_pos[1],
                        max_pos[2],
                    ]
                )

            if split_dir == "y direction":
                tempt_min_pos = min_pos + np.array(
                    [0, culmulative_percentage * scope[1], 0]
                )
                culmulative_percentage += new_obj_info[2]
                tempt_max_pos = np.array(
                    [
                        max_pos[0],
                        min_pos[1] + culmulative_percentage * scope[1],
                        max_pos[2],
                    ]
                )

            if split_dir == "z direction":
                tempt_min_pos = min_pos + np.array(
                    [0, 0, culmulative_percentage * scope[2]]
                )
                culmulative_percentage += new_obj_info[2]
                tempt_max_pos = np.array(
                    [
                        max_pos[0],
                        max_pos[1],
                        min_pos[2] + culmulative_percentage * scope[2],
                    ]
                )

            if new_obj_info[0] == "nonterminal":
                new_instance_nonterminal_object = instance_nonterminal_object(
                    new_obj_info[1], tempt_min_pos, tempt_max_pos
                )
                nonterminal_list.append(new_instance_nonterminal_object)

            if new_obj_info[0] == "terminal":
                generic_terminal_object = self.generic_terminal_list[
                    int(new_obj_info[1])
                ]
                multiplier = generic_terminal_object.multiplier
                if (
                    multiplier[0] != 0.001
                    and multiplier[1] != 0.001
                    and multiplier[2] != 0.001
                ):
                    rule = generic_terminal_object.rule
                    object_size = (tempt_max_pos - tempt_min_pos) * 0.5 * multiplier

                    terminal_list += self.produce_terminal_instance(
                        rule,
                        object_size,
                        tempt_max_pos,
                        tempt_min_pos,
                        new_obj_info[1],
                        rotation,
                        group,
                    )

        return (nonterminal_list, terminal_list)

    def produce_terminal_instance(
        self,
        rule,
        object_size,
        tempt_max_pos,
        tempt_min_pos,
        terminal_type,
        rotation,
        group,
    ):
        instance_list = []
        if rule == "normal":
            new_instance_terminal_object = instance_terminal_object(
                terminal_type, tempt_min_pos, tempt_max_pos, rotation, group
            )
            new_instance_terminal_object.set_position(
                (tempt_min_pos + tempt_max_pos) * 0.5
            )
            instance_list.append(new_instance_terminal_object)

        # if rule == "four_corners":
        #     new_instance_terminal_object_0 = instance_terminal_object(terminal_type, tempt_min_pos, tempt_max_pos, rotation)
        #     new_instance_terminal_object_1 = instance_terminal_object(terminal_type, tempt_min_pos, tempt_max_pos, rotation)
        #     new_instance_terminal_object_2 = instance_terminal_object(terminal_type, tempt_min_pos, tempt_max_pos, rotation)
        #     new_instance_terminal_object_3 = instance_terminal_object(terminal_type, tempt_min_pos, tempt_max_pos, rotation)

        #     new_instance_terminal_object_0.set_position(tempt_min_pos + object_size)
        #     new_instance_terminal_object_1.set_position(np.array([tempt_max_pos[0],tempt_min_pos[1],tempt_min_pos[2]]) + np.array([-object_size[0], object_size[1], object_size[2]]))
        #     new_instance_terminal_object_2.set_position(np.array([tempt_min_pos[0],tempt_min_pos[1],tempt_max_pos[2]]) + np.array([object_size[0], object_size[1], -object_size[2]]))
        #     new_instance_terminal_object_3.set_position(np.array([tempt_max_pos[0],tempt_min_pos[1],tempt_max_pos[2]]) + np.array([-object_size[0], object_size[1], -object_size[2]]))

        #     instance_list.append(new_instance_terminal_object_0)
        #     instance_list.append(new_instance_terminal_object_1)
        #     instance_list.append(new_instance_terminal_object_2)
        #     instance_list.append(new_instance_terminal_object_3)

        for obj in instance_list:
            obj.set_size(object_size)

        return instance_list


class generic_footprint_object:
    def __init__(self, info):
        self.structural_id = info["structural_id"]
        self.subdiv = info["subdiv"]

    def execute_subdiv(self):
        seed = random.uniform(0, 1)
        culmulative_prob = 0

        for subdiv_rule in self.subdiv:
            culmulative_prob += subdiv_rule[0]
            if culmulative_prob >= seed:
                break

        return subdiv_rule


class generic_nonterminal_object:
    def __init__(self, info):
        self.nonterminal_id = info["nonterminal_id"]
        self.subdiv = info["subdiv"]

    def execute_subdiv(self):
        seed = random.uniform(0, 1)
        culmulative_prob = 0

        for subdiv_rule in self.subdiv:
            culmulative_prob += subdiv_rule[0]
            if culmulative_prob >= seed:
                break

        return subdiv_rule


class generic_terminal_object:
    def __init__(self, info):
        self.terminal_id = info["terminal_id"]
        self.rule = info["rule"]
        self.multiplier = info["multiplier"]


class instance_nonterminal_object:
    def __init__(self, type, min_pos, max_pos):
        self.type = type
        self.min_pos = min_pos
        self.max_pos = max_pos


class instance_terminal_object:
    def __init__(self, type, min_pos, max_pos, rotation, group):
        self.type = type
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.rotation = rotation
        self.group = group

    def set_position(self, position):
        self.position = position

    def set_size(self, size):
        self.size = size
