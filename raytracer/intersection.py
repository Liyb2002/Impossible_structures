import taichi as ti
import numpy as np
import argparse
import random

from ray_tracing_models import Ray, Camera, Hittable_list, Sphere, PI, xy_rect, xz_rect, yz_rect
ti.init(arch=ti.gpu)

@ti.data_oriented
class Scene:
    def __init__(self):
        self.possible_intersects = ti.Vector.field(3, dtype=ti.f32, shape=(25))
        self.max_screen = ti.Vector.field(2, dtype=ti.f32, shape=(25))
        self.min_screen = ti.Vector.field(2, dtype=ti.f32, shape=(25))

        self.x_start = 400
        self.y_start = 400
        self.image_height = 800
        self.image_width = 800

        self.camera = Camera()
        self.get_impossible_intersection()
        

    
    @ti.kernel
    def get_impossible_intersection(self):
        u = (self.x_start) / self.image_width
        v = (self.y_start) / self.image_height
        ray = self.camera.get_ray(u, v)
        ray_max = self.camera.get_ray(1, 1)
        ray_min = self.camera.get_ray(0, 0)

        for k in range(5,25):
            x = ray.origin[0] + ray.direction[0] * (k*0.25)
            y = ray.origin[1] + ray.direction[1] * (k*0.25)
            z = ray.origin[2] + ray.direction[2] * (k*0.25)
            pos = ti.Vector([x, y,z])
            self.possible_intersects[k] += pos

            x_max = ray_max.origin[0] + ray_max.direction[0] * (k*0.25)
            y_max = ray_max.origin[1] + ray_max.direction[1] * (k*0.25)
            pos_max = ti.Vector([x_max, y_max])
            self.max_screen[k] += pos_max

            x_min = ray_min.origin[0] + ray_min.direction[0] * (k*0.25)
            y_min = ray_min.origin[1] + ray_min.direction[1] * (k*0.25)
            pos_min = ti.Vector([x_min, y_min])
            self.min_screen[k] += pos_min

    def get_max_screen(self, k):
        return np.array([self.max_screen[k][0], self.max_screen[k][1]])
    
    def get_min_screen(self, k):
        return np.array([self.min_screen[k][0], self.min_screen[k][1]])
    
    def get_possible_intersects(self, k):
        return np.array([self.possible_intersects[k][0], self.possible_intersects[k][1], self.possible_intersects[k][2]])