import numpy as np
import random
from . import procedural_objects


class box:
    def __init__(self, position, scope):
        self.position = position
        self.scope = scope

    def check_within(self, obj):
        cuboidA_min = [self.position[i] - self.scope[i] for i in range(3)]
        cuboidA_max = [self.position[i] + self.scope[i] for i in range(3)]

        # Calculate the minimum and maximum coordinates of cuboid B
        cuboidB_min = [obj.position[i] - obj.length[i] for i in range(3)]
        cuboidB_max = [obj.position[i] + obj.length[i] for i in range(3)]

        # Check if cuboid B is strictly contained within cuboid A
        for i in range(3):
            if not (cuboidA_min[i] < cuboidB_min[i] < cuboidB_max[i] < cuboidA_max[i]):
                return False

        return True
