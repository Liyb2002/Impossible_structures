from . import generic_objects
from . import procedural_objects
import numpy as np


def execute_model(generic_object_list, start_obj, steps):
    production_list = []

    cur_obj = start_obj
    production_list.append(cur_obj)

    # processing
    count = 0
    not_end = True
    while count < steps or not_end:
        tempt_count = count
        next_type = None

        while tempt_count >= 0 and next_type == None:
            cur_obj = production_list[tempt_count]
            cur_type = production_list[tempt_count].type
            cur_generic_obj = generic_object_list[cur_type]
            next_type = cur_generic_obj.get_nextType(cur_obj.connected)
            tempt_count -= 1

        if next_type == None:
            return []

        next_generic_obj = generic_object_list[next_type]
        next_scope = next_generic_obj.scope
        next_hash = next_generic_obj.generate_hash()
        next_rotation = next_generic_obj.rotation
        next_offset = cur_generic_obj.get_offset(next_type)
        next_obj = procedural_objects.Procedural_object(
            next_type,
            np.array([0, 0, 0]),
            next_scope,
            next_hash,
            next_rotation,
            next_offset,
        )
        next_choice = cur_generic_obj.execute_rule(next_type)
        cur_obj.add_connected(next_choice)
        next_obj.add_connected(opposite_direction(next_choice))
        next_obj.set_position(cur_obj, next_choice)

        production_list.append(next_obj)
        cur_obj = next_obj

        if next_generic_obj.canTerminate == "False":
            not_end = True
        else:
            not_end = False

        count += 1
    production_list.pop(0)
    return production_list


class connect_execution:
    def __init__(
        self, objStart, generic_object_list, delta, direction, available_endings, objEnd
    ):
        self.objStart = objStart
        self.generic_object_list = generic_object_list
        self.delta = delta
        self.direction = direction
        self.available_endings = available_endings
        self.objEnd = objEnd

        self.direction_idx = direction_to_index(self.direction)

        self.lower_bound = self.objStart.length[self.direction_idx]
        self.current_bound = self.objStart.length[self.direction_idx]
        self.upper_bound = self.objStart.length[self.direction_idx]

        self.prev_lower_bound = 0
        self.prev_current_bound = 0
        self.prev_upper_bound = 0

        self.current_type = self.objStart.type
        self.cur_obj = self.objStart

        self.production_list = []
        self.rules_list = []

    def execute_model_withDirection(self):
        # return 0->fail, 1->continue, 2->end
        # execute rule to get the objects
        current_generic_obj = self.generic_object_list[self.current_type]

        ok, next_type, rule_chosen = current_generic_obj.get_nextType_with_direction(
            self.direction
        )
        if ok != True:
            # print("current type", current_generic_obj.id, "target direction", self.direction)
            # print("can't find next object available")
            return 0
        next_type = int(next_type)

        next_generic_obj = self.generic_object_list[next_type]
        if next_generic_obj.cycle_connect == "False":
            return 0
        next_scope = next_generic_obj.scope
        next_hash = next_generic_obj.generate_hash()
        next_rotation = next_generic_obj.rotation
        next_offset = current_generic_obj.get_offset(next_type)
        next_obj = procedural_objects.Procedural_object(
            next_type,
            np.array([0, 0, 0]),
            next_scope,
            next_hash,
            next_rotation,
            next_offset,
        )
        self.cur_obj.add_connected(rule_chosen)
        next_obj.add_connected(opposite_direction(rule_chosen))
        self.production_list.append(next_obj)
        self.rules_list.append(rule_chosen)

        if self.direction_idx != 2:
            self.lower_bound += (
                next_scope[self.direction_idx][0] + self.prev_lower_bound
            )
            self.current_bound += (
                next_obj.length[self.direction_idx] + self.prev_current_bound
            )
            self.upper_bound += (
                next_scope[self.direction_idx][1] + self.prev_upper_bound
            )
            self.prev_lower_bound = next_scope[self.direction_idx][0]
            self.prev_current_bound = next_obj.length[self.direction_idx]
            self.prev_upper_bound = next_scope[self.direction_idx][1]
        elif self.objEnd.type == 3 or self.objEnd.type == 8:
            self.lower_bound += (
                next_scope[self.direction_idx][0] + self.prev_lower_bound
            )
            self.current_bound += (
                next_obj.length[self.direction_idx] + self.prev_current_bound
            )
            self.upper_bound += (
                next_scope[self.direction_idx][1] + self.prev_upper_bound
            )
            self.prev_lower_bound = next_scope[self.direction_idx][0]
            self.prev_current_bound = next_obj.length[self.direction_idx]
            self.prev_upper_bound = next_scope[self.direction_idx][1]
        else:
            self.lower_bound += next_scope[self.direction_idx][0] * 2
            self.current_bound += next_obj.length[self.direction_idx] * 2
            self.upper_bound += next_scope[self.direction_idx][1] * 2

        self.current_type = next_type

        if (
            self.upper_bound > self.delta[self.direction_idx]
            and self.lower_bound < self.delta[self.direction_idx]
            and valid_ending(self.available_endings, self.current_type)
        ):
            return 2

        if self.lower_bound > self.delta[self.direction_idx]:
            # print("lower bound larger than delta")
            return 0

        return 1

    def set_scope(self):
        # find exact scope of the objects
        if self.current_bound < self.delta[self.direction_idx]:
            self.production_list = add_scope(
                self.current_bound, self.delta, self.production_list, self.direction_idx
            )

        if self.current_bound > self.delta[self.direction_idx]:
            self.production_list = minus_scope(
                self.current_bound, self.delta, self.production_list, self.direction_idx
            )

        # production_list = adjust_scope(production_list)

        # set object positions
        first_obj = self.production_list[0]
        first_obj.set_position(self.objStart, self.rules_list[0])
        for i in range(1, len(self.production_list)):
            prev_obj = self.production_list[i - 1]
            self.cur_obj = self.production_list[i]
            self.cur_obj.set_position(prev_obj, self.rules_list[i])

        return self.production_list


def add_scope(current_bound, delta, production_list, direction_idx):
    # print("do add scope")
    for obj in production_list:
        target_add = delta[direction_idx] - current_bound
        available_add = (obj.scope[direction_idx][1] - obj.length[direction_idx]) * 2
        if target_add > available_add:
            obj.length[direction_idx] = obj.scope[direction_idx][1]
            current_bound += available_add
        else:
            obj.length[direction_idx] += target_add * 0.5
            break
    return production_list


def minus_scope(current_bound, delta, production_list, direction_idx):
    # print("do minus scope")
    for obj in production_list:
        target_minus = current_bound - delta[direction_idx]
        available_minus = (obj.length[direction_idx] - obj.scope[direction_idx][0]) * 2
        if target_minus > available_minus:
            obj.length[direction_idx] = obj.scope[direction_idx][0]
            current_bound -= available_minus
        else:
            obj.length[direction_idx] -= target_minus * 0.5
            break
    return production_list


def adjust_scope(production_list):
    target_adjust = production_list[-1].length[0]
    for obj in production_list:
        available_adjust = (obj.length[0] - obj.scope[0][0]) * 2
        if target_adjust > available_adjust:
            obj.length[0] = obj.scope[0][0]
            target_adjust -= available_adjust
        else:
            obj.length[0] -= target_adjust * 0.5
            break
    return production_list


def direction_to_index(direction):
    if direction == "+x" or direction == "-x":
        return 0

    if direction == "+y" or direction == "-y":
        return 1

    return 2


def valid_ending(available_endings, cur_type):
    for ending in available_endings:
        if ending == cur_type:
            return True

    return False


def update_delta(direction, delta, start_obj):
    if direction == "+x" or direction == "-x":
        delta -= np.array([start_obj.length[0], 0, 0])

    if direction == "+y" or direction == "-y":
        delta -= np.array([0, start_obj.length[1], 0])

    if direction == "+z" or direction == "-z":
        delta -= np.array([0, 0, start_obj.length[2]])


def opposite_direction(direction):
    if direction == "+x":
        return "-x"
    if direction == "-x":
        return "+x"
    if direction == "+y":
        return "-y"
    if direction == "-y":
        return "+y"
    if direction == "+z":
        return "-z"
    if direction == "-z":
        return "+z"

    return "+x"
