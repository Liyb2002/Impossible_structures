import numpy as np
import argparse
import random

import perspective

class Scene:
    def __init__(self, startPos):
        self.possible_intersects = []
        self.max_screen = []
        self.min_screen = []

        self.x_start = startPos[0]
        self.y_start = startPos[1]
        self.image_height = 800
        self.image_width = 800

        self.camera = perspective.Camera()
        self.get_impossible_intersection()
        

    def get_impossible_intersection(self):
        u = (self.x_start) / self.image_width
        v = (self.y_start) / self.image_height
        camera_pos = self.camera.get_camera_origin()
        ray = self.camera.get_ray(u, v)

        ray_max = self.camera.get_ray(1, 1)
        ray_min = self.camera.get_ray(0, 0)

        for k in range(0,40):
            x = camera_pos[0] + ray[0] * (k*0.5)
            y = camera_pos[1] + ray[1] * (k*0.5)
            z = camera_pos[2] + ray[2] * (k*0.5)
            pos = np.array([x, y,z])
            self.possible_intersects.append(pos)

            x_max = camera_pos[0] + ray_max[0] * (k*0.5)
            y_max = camera_pos[1] + ray_max[1] * (k*0.5)
            pos_max = np.array([x_max, y_max])
            self.max_screen.append(pos_max)

            x_min = camera_pos[0] + ray_min[0] * (k*0.5)
            y_min = camera_pos[1] + ray_min[1] * (k*0.5)
            pos_min = np.array([x_min, y_min])
            self.min_screen.append(pos_min)

    def get_intersection_t(self, screenPos, worldPos):
        u = (screenPos[0]) / self.image_width
        v = (screenPos[1]) / self.image_height
        camera_pos = self.camera.get_camera_origin()
        ray = self.camera.get_ray(u, v)

        t = (worldPos[2] - camera_pos[2]) / ray[2]
        x = camera_pos[0] + ray[0] * t
        y = camera_pos[1] + ray[1] * t

        return np.array([x, y, worldPos[2]])


    def get_max_screen(self, k):
        return np.array([self.max_screen[k][0], self.max_screen[k][1]])
    
    def get_min_screen(self, k):
        return np.array([self.min_screen[k][0], self.min_screen[k][1]])
    
    def get_possible_intersects(self, k):
        return np.array([self.possible_intersects[k][0], self.possible_intersects[k][1], self.possible_intersects[k][2]])