import numpy as np
import random
import structure

def offset():
    num = round(int(random.random() * 5 % 5) * 0.1 + 0.2, 1)
    sign = random.random()
    if(sign > 0.5):
        return num
    return -num

class connecting_structure:
    def __init__(self, x, y, foreground_z, background_z):
        self.x = x
        self.y = y
        self.foreground_z = foreground_z
        self.background_z = background_z
    
    def get_object(self):
        z_start = min(self.foreground_z, self.background_z)
        z_scale = abs(self.foreground_z - self.background_z )
        
        startPos = np.array([self.x,self.y,z_start])
        scale = np.array([0.07, 0.07, z_scale])
        
        tempt = structure.rect(startPos, scale)
        
        return tempt
    
    def get_center(self):
        z_start = min(self.foreground_z, self.background_z)
        z_scale = abs(self.foreground_z - self.background_z )
        
        center = np.array([self.x+0.035, self.y+0.035, z_start + 0.5*z_scale])
        
        return center

    def xy_pos(self):
        return np.array([self.x, self.y])
    
    def get_sample_points(self):
        start = self.foreground_z
        end = self.background_z
        dist = abs(start - end)
        i = 0.05
        points_list = []

        while i < dist:
            random_x = round(random.uniform(1, 6)/100,2)
            random_y = round(random.uniform(1, 6)/100,2)

            point = np.array([self.x + random_x, self.y + random_y, end + i])
            points_list.append(point)
            i += 0.05

        return points_list

