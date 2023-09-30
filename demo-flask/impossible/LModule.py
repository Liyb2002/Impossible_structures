from . import procedural_objects
import numpy as np
import random
import math


class Module:
    def __init__(self, position, size, rotation, age, type):
        self.type = type
        self.position = position
        self.size = size
        self.age = age + 1
        self.rotation = rotation

        # print("position", self.position)

    def toProcedual(self):
        dummy_scope = [0.1, 0.1]
        tempt_obj = procedural_objects.Procedural_object(
            self.type,
            self.position,
            np.array([dummy_scope, dummy_scope, dummy_scope]),
            "00000",
            np.array([[self.rotation[0]], [self.rotation[1]], [self.rotation[2]]]),
            np.array([0, 0, 0]),
        )
        tempt_obj.arbitrary_set_length(
            np.array([float(self.size[0]), float(self.size[1]), float(self.size[2])])
        )
        return tempt_obj

    def execute(self, origin, rotation, light_pos, rules):
        # to world position
        world_pos = compute_world_position(self.position, origin, rotation)

        origin_dist = math.sqrt(
            (origin[0] - light_pos[0]) ** 2
            + (origin[1] - light_pos[1]) ** 2
            + (origin[2] - light_pos[2]) ** 2
        )
        pt_dist = math.sqrt(
            (world_pos[0] - light_pos[0]) ** 2
            + (world_pos[1] - light_pos[1]) ** 2
            + (world_pos[2] - light_pos[2]) ** 2
        )
        dist_factor = 1 - (origin_dist * 0.1)
        # chose a rule to execute
        execute_rule = None
        new_modules = []

        for rule in rules:
            if rule.lhs_type == self.type and self.satify_condition(rule, dist_factor):
                execute_rule = rule
                break

        if not execute_rule:
            return []

        for i in range(len(execute_rule.rhs_types)):
            # prob = max(execute_rule.prob_each[i] * dist_factor, 0.1)
            rand = random.random()
            p = execute_rule.prob_each[i]
            if rand < p:
                new_type = execute_rule.rhs_types[i]
                new_size = np.array(
                    [
                        self.size[0] * execute_rule.rhs_size_multiplier[i][0],
                        self.size[1] * execute_rule.rhs_size_multiplier[i][1],
                        self.size[2] * execute_rule.rhs_size_multiplier[i][2],
                    ]
                )
                new_rotation = self.rotation + execute_rule.rhs_rotations[i]
                new_direction = execute_rule.rhs_directions[i]
                new_offsets = execute_rule.rhs_offsets[i]

                new_position = self.get_new_position(
                    new_direction, new_size, new_offsets
                )
                new_module = Module(
                    new_position,
                    new_size,
                    new_rotation,
                    self.age,
                    execute_rule.rhs_types[i],
                )
                new_modules.append(new_module)

        return new_modules

    def get_new_position(self, new_directions, new_size, new_offsets):
        new_position = self.position + new_offsets

        for new_direction in new_directions:
            if new_direction[0] == "+x":
                prev_obj_closest_point = self.position + np.array([self.size[0], 0, 0])
                prev_obj_rotated_point = procedural_objects.rotate_line(
                    self.position,
                    prev_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

                new_obj_closest_point = np.array([new_size[0], 0, 0])
                new_obj_rotated_point = procedural_objects.rotate_line(
                    np.array([0, 0, 0]),
                    new_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

                new_position += (
                    np.array([self.size[0], 0, 0])
                    + np.array([new_size[0], 0, 0])
                    + prev_obj_delta_rotate
                    + new_obj_delta_rotate
                ) * new_direction[1]

            if new_direction[0] == "+y":
                prev_obj_closest_point = self.position + np.array([0, self.size[1], 0])
                prev_obj_rotated_point = procedural_objects.rotate_line(
                    self.position,
                    prev_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

                new_obj_closest_point = np.array([0, new_size[1], 0])
                new_obj_rotated_point = procedural_objects.rotate_line(
                    np.array([0, 0, 0]),
                    new_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

                new_position += (
                    np.array([0, self.size[1], 0])
                    + np.array([0, new_size[1], 0])
                    + prev_obj_delta_rotate
                    + new_obj_delta_rotate
                ) * new_direction[1]

            if new_direction[0] == "-y":
                prev_obj_closest_point = self.position - np.array([0, self.size[1], 0])
                prev_obj_rotated_point = procedural_objects.rotate_line(
                    self.position,
                    prev_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

                new_obj_closest_point = np.array([0, -new_size[1], 0])
                new_obj_rotated_point = procedural_objects.rotate_line(
                    np.array([0, 0, 0]),
                    new_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

                new_position += (
                    0
                    - np.array([0, self.size[1], 0])
                    - np.array([0, new_size[1], 0])
                    + prev_obj_delta_rotate
                    + new_obj_delta_rotate
                ) * new_direction[1]

            if new_direction[0] == "+z":
                prev_obj_closest_point = self.position + np.array([0, 0, self.size[2]])
                prev_obj_rotated_point = procedural_objects.rotate_line(
                    self.position,
                    prev_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

                new_obj_closest_point = np.array([0, 0, new_size[2]])
                new_obj_rotated_point = procedural_objects.rotate_line(
                    np.array([0, 0, 0]),
                    new_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

                new_position += (
                    np.array([0, 0, self.size[2]])
                    + np.array([0, 0, new_size[2]])
                    + prev_obj_delta_rotate
                    + new_obj_delta_rotate
                ) * new_direction[1]

            if new_direction[0] == "-z":
                prev_obj_closest_point = self.position - np.array([0, 0, self.size[2]])
                prev_obj_rotated_point = procedural_objects.rotate_line(
                    self.position,
                    prev_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

                new_obj_closest_point = np.array([0, 0, -new_size[2]])
                new_obj_rotated_point = procedural_objects.rotate_line(
                    np.array([0, 0, 0]),
                    new_obj_closest_point,
                    self.rotation[0],
                    self.rotation[1],
                    self.rotation[2],
                )
                new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

                new_position += (
                    0
                    - np.array([0, 0, self.size[2]])
                    - np.array([0, 0, new_size[2]])
                    + prev_obj_delta_rotate
                    + new_obj_delta_rotate
                ) * new_direction[1]

        return new_position

    def satify_condition(self, rule, dist_factor):
        for condition in rule.condition:
            if condition[0] == "age":
                if condition[1] == "less_than" and self.age >= condition[2]:
                    return False

                if condition[1] == "larger_than" and self.age <= condition[2]:
                    return False

            if condition[0] == "Prob" and random.random() < condition[1]:
                return False

        return True


def compute_world_position(position, translation, rotation):
    """Compute the world position after translation and rotations."""
    translation_vector = np.array(translation)
    position_vector = np.array(position)

    # Apply translation
    translated_position = position_vector + translation_vector

    # Apply rotations
    rotated_position = rotate_vector(translated_position, rotation)

    return translated_position


def rotate_vector(vector, rotation):
    """Rotate a vector by the specified Euler angles."""
    rx, ry, rz = rotation
    # Create rotation matrices
    Rx = np.array(
        [[1, 0, 0], [0, np.cos(rx), -np.sin(rx)], [0, np.sin(rx), np.cos(rx)]]
    )
    Ry = np.array(
        [[np.cos(ry), 0, np.sin(ry)], [0, 1, 0], [-np.sin(ry), 0, np.cos(ry)]]
    )
    Rz = np.array(
        [[np.cos(rz), -np.sin(rz), 0], [np.sin(rz), np.cos(rz), 0], [0, 0, 1]]
    )
    # Apply rotations in the order: Rz * Ry * Rx
    rotated_vector = np.dot(Rz, np.dot(Ry, np.dot(Rx, vector)))
    return rotated_vector
