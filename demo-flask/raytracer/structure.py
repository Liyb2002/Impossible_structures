import numpy as np
import random


class Structure:
    def __init__(self, seed, seed_next_possible, portion, block_size, layer=None):
        self.history = None
        self.data = None
        self.rect = []
        self.next_possibles = None
        self.layer = layer

        self.portion = portion
        self.seed = seed
        self.seed_next_possible = seed_next_possible

        self.min_x = 1000
        self.max_x = -1000
        self.min_y = 1000
        self.max_y = -1000

        self.block_size = block_size

        self.cleanUp()

        # print("initialized data: \n", self.data)

    def to_dest_1(self, destination):
        for i in destination:
            next_vertex = self.next_possibles[0]
            x_dist = abs(i[0] - next_vertex[0])
            x_start = min(i[0], next_vertex[0])
            startPos = np.array([x_start, next_vertex[1], next_vertex[2]])
            scale = np.array(
                [
                    x_dist + self.block_size * self.portion,
                    self.block_size * self.portion,
                    self.block_size * self.portion,
                ]
            )
            rect1 = rect(startPos, scale)
            self.rect.append(rect1)

    def to_dest_2(self, destination):
        for i in destination:
            next_vertex = self.next_possibles[0]
            y_dist = abs(i[1] - next_vertex[1])
            y_start = min(i[1], next_vertex[1])
            startPos2 = np.array([i[0], y_start, next_vertex[2]])
            scale2 = np.array(
                [
                    self.block_size,
                    y_dist + self.block_size * self.portion,
                    self.block_size * self.portion,
                ]
            )
            rect2 = rect(startPos2, scale2)
            self.rect.append(rect2)

    def cleanUp(self):
        self.history = self.seed
        self.data = np.array([[0.0, 0.0, 0.0]])
        self.data = np.append(self.data, self.seed, axis=0)
        self.rect = []
        self.rect.append(block_to_rect(self.data, self.portion, self.block_size))
        self.data = np.array([[0.0, 0.0, 0.0]])
        self.next_possibles = self.seed_next_possible

    def get_MaxMin(self):
        for i in self.rect:
            x_1 = i.start_x
            x_2 = i.start_x + i.scale_x
            y_1 = i.start_y
            y_2 = i.start_y + i.scale_y

            if x_1 < self.min_x:
                self.min_x = x_1
            if x_2 > self.max_x:
                self.max_x = x_2
            if y_1 < self.min_y:
                self.min_y = y_1
            if y_2 > self.max_y:
                self.max_y = y_2

    def cost_func(self, pos):
        return random.random()

    def add_vertex(self, next_vertex):
        x = next_vertex[0]
        y = next_vertex[1]
        z = next_vertex[2]

        self.data = np.vstack([self.data, np.array([x, y, z])])

    def remove_possible(self, next_index):
        self.next_possibles = np.delete(self.next_possibles, next_index, axis=0)

    # define direction:
    # x=-1 -> 0, x=1 -> 1, y=-1 -> 2, y=1 -> 3, z=-1 -> 4, z=1 -> 5,
    def get_next_possible(self, available_contact, direction):
        result = np.array([0, 0, 0, 0])

        available_contact = np.append(available_contact, 0)
        if direction == 0 or direction == 1:
            result = np.vstack(
                [result, available_contact + np.array([0.0, self.block_size, 0.0, 3])]
            )
            result = np.vstack(
                [result, available_contact + np.array([0.0, -self.block_size, 0.0, 2])]
            )
            result = np.delete(result, 0, axis=0)
            return result

        if direction == 2 or direction == 3:
            result = np.vstack(
                [result, available_contact + np.array([self.block_size, 0.0, 0.0, 1])]
            )
            result = np.vstack(
                [result, available_contact + np.array([-self.block_size, 0.0, 0.0, 1])]
            )
            result = np.delete(result, 0, axis=0)
            return result

    def get_last_direction(self, direction):
        count = direction[1] * 1 + direction[2] * 2
        return count

    def get_vertex_forward(self, new_vertex_clean, direction):
        if direction == 0:
            return new_vertex_clean + np.array([-self.block_size, 0.0, 0.0])

        if direction == 1:
            return new_vertex_clean + np.array([self.block_size, 0.0, 0.0])

        if direction == 2:
            return new_vertex_clean + np.array([0.0, -self.block_size, 0.0])

        if direction == 3:
            return new_vertex_clean + np.array([0.0, self.block_size, 0.0])

    def generate(self, steps, beam_mean, beam_sd):
        for i in range(steps):
            # print("step ", i+1)
            self.process(beam_mean, beam_sd)
            self.history = np.append(self.history, self.data[1:], axis=0)
            self.rect.append(block_to_rect(self.data, self.portion, self.block_size))
            self.data = np.array([[0, 0, 0]])

    def process(self, beam_mean, beam_sd):
        # step 1: for all available contacts, assume they will make a turn
        # print("next_possibles", self.next_possibles)

        # step2: create a 1d array that stores cost for each possible point
        costs = np.array([])
        for next_possible in self.next_possibles:
            costs = np.append(costs, self.cost_func(next_possible))

        # print("costs", costs)

        # step3 find the next_vertex with smallest cost
        next_index = np.argpartition(costs, -1)[-1:]
        next_vertex = self.next_possibles[next_index]

        # print("next_vertex", next_vertex)

        # step4 add next_vertex to data
        new_direction = next_vertex[0][3]
        # print("new_direction", new_direction)
        new_vertex_clean = np.array(
            [next_vertex[0][0], next_vertex[0][1], next_vertex[0][2]]
        )
        # print("new_vertex_clean", new_vertex_clean)
        self.add_vertex(new_vertex_clean)

        span = int(np.random.normal(loc=beam_mean - 2, scale=beam_sd, size=None)) + 2
        for i in range(span):
            new_vertex_clean = self.get_vertex_forward(new_vertex_clean, new_direction)
            self.add_vertex(new_vertex_clean)

        # print("data: \n", self.data)

        # step5 update next_possible
        self.remove_possible(next_index)
        # print("next_possibles, removed old", self.next_possibles)
        # print("next_vertex", new_vertex_clean)
        # print("new_direction", new_direction)
        new_next_possibles = self.get_next_possible(new_vertex_clean, new_direction)
        self.next_possibles = np.append(self.next_possibles, new_next_possibles, axis=0)
        # print("next_possibles, add new", self.next_possibles)


class rect:
    def __init__(self, startPos, scale):
        self.start_x = round(startPos[0], 2)
        self.start_y = round(startPos[1], 2)
        self.start_z = round(startPos[2], 2)

        self.scale_x = round(scale[0], 2)
        self.scale_y = round(scale[1], 2)
        self.scale_z = round(scale[2], 2)

    def info(self):
        print(
            "start_x:", self.start_x, "start_y:", self.start_y, "start_z:", self.start_z
        )
        print(
            "scale_x:", self.scale_x, "scale_y:", self.scale_y, "scale_z:", self.scale_z
        )
        print(" ")

    def center(self):
        return np.array(
            [
                self.start_x + self.scale_x / 2,
                self.start_y + self.scale_y / 2,
                self.start_z + self.scale_z / 2,
                1,
            ]
        )


def block_to_rect(buffer, portion, block_size):
    start = buffer[1]
    end = buffer[-1]
    x_start = min(start[0], end[0])
    y_start = min(start[1], end[1])
    z_start = min(start[2], end[2])

    x_scale = max(abs(start[0] - end[0]), block_size * portion)
    y_scale = max(abs(start[1] - end[1]), block_size * portion)
    z_scale = max(abs(start[2] - end[2]), block_size * portion)

    if x_scale > block_size * portion:
        x_scale += block_size * portion

    if y_scale > block_size * portion:
        y_scale += block_size * portion

    if z_scale > block_size * portion:
        z_scale += block_size * portion

    startPos = np.array([x_start, y_start, z_start])
    scale = np.array([x_scale, y_scale, z_scale])

    tempt = rect(startPos, scale)
    return tempt


def check_close(struct_a, struct_b):
    for i in struct_a.rect:
        for j in struct_b.rect:
            dist_x = abs(i.center_x() - j.center_x())
            dist_y = abs(i.center_y() - j.center_y())

            if dist_x < 0.2 or dist_y < 0.2:
                return True
    return False


def rand_index(input_array):
    return int(random.random() * len(input_array) % len(input_array))
