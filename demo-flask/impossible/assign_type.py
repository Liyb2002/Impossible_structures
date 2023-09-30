import copy
import random
import numpy as np

def assign(procedural_objects):
    for obj in procedural_objects:
        
        if obj.type == 1:
            assign_available = True
            for dir in obj.connected:
                if dir == "+y":
                    assign_available = False
            
            if assign_available:
                offset = random.uniform(0.1, 0.2)
                obj.position += np.array([0, offset, 0])
                obj.length += np.array([0, offset, 0])
                obj.type = 9
    
    return procedural_objects
