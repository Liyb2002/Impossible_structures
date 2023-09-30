from . import LModule
from . import procedural_objects

import json
import numpy as np


class LSys:
    def __init__(self):
        self.alpha = 0.4
        self.min_light = 0.1
        self.max_age = 5
        self.bounding_box = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
        self.steps = 7
        self.procedural_objects = []
        self.new_objects = []
        self.rules = []

    def system_setup(
        self,
        origin,
        system_rotation,
        group_id,
        light_pos,
        sys_path="tree/LSystem.json",
        init_size=np.array([0.2, 0.025, 0.025]),
    ):
        self.origin = origin
        self.system_rotation = system_rotation
        self.group = group_id
        self.light_pos = light_pos
        self.sys_path = sys_path

        self.add_rules()
        self.init_state(init_size)

    def init_state(self, init_size=np.array([0.2, 0.025, 0.025])):
        start_module = LModule.Module(
            position=np.array([0, 0, 0]),
            size=init_size,
            rotation=np.array([0, 0, 0]),
            age=1,
            type=11,
        )
        self.new_objects.append(start_module)

    def run_system(self):
        for i in range(0, self.steps):
            self.run_step()

    def run_step(self):
        level_count = len(self.new_objects)
        count = 1
        for obj in self.new_objects:
            if count > level_count:
                break
            count += 1
            self.new_objects += obj.execute(
                self.origin, self.system_rotation, self.light_pos, self.rules
            )
            self.procedural_objects.append(obj.toProcedual())

    def add_rules(self):
        with open(self.sys_path, "r") as object_file:
            rules_json = json.load(object_file)
            for rule_json in rules_json:
                new_rule = rule(rule_json)
                self.rules.append(new_rule)

    def finish_system(self):
        for obj in self.new_objects:
            self.procedural_objects.append(obj.toProcedual())

        for obj in self.procedural_objects:
            obj.set_group(self.group)

        return self.procedural_objects


class rule:
    def __init__(self, rule_json):
        self.lhs_type = rule_json["lhs_type"]
        self.rhs_types = rule_json["rhs_types"]
        self.rhs_size_multiplier = rule_json["rhs_size_multiplier"]
        self.rhs_rotations = rule_json["rhs_rotations"]
        self.rhs_offsets = rule_json["rhs_offsets"]
        self.rhs_directions = rule_json["rhs_directions"]
        self.condition = rule_json["condition"]
        self.prob_each = rule_json["prob_each"]
