import numpy as np
import math

PI = 3.1415

class Camera:
    def __init__(self, fov=60, aspect_ratio=1.0):
        # Camera parameters
        self.lookfrom = np.array((0.4, 0.5, 2.0))
        self.lookat = np.array([0.0, 0.0, 0.0])
        self.vup = np.array([0.0, 1.0, 0.0])
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        
        theta = self.fov * (PI / 180.0)
        half_height = math.tan(theta / 2.0)
        half_width = self.aspect_ratio * half_height
        
        self.cam_origin = self.lookfrom
        
        w = self.lookfrom - self.lookat
        w = w / np.linalg.norm(w)

        u = np.cross(self.vup, w)
        u = u / np.linalg.norm(u)
        
        v = np.cross(w, u)
        
        self.cam_lower_left_corner = self.cam_origin - half_width * u - half_height * v - w
        self.cam_horizontal = 2 * half_width * u
        self.cam_vertical = 2 * half_height * v
    
    def test(self):
        print("test")
    
    def get_direction(self, u, v):
        
        u = (u) / 1280
        v = (v) / 720

        direction = self.cam_lower_left_corner + u * self.cam_horizontal + v * self.cam_vertical - self.cam_origin
        #direction = direction / np.linalg.norm(direction)
        
#         print("self.cam_lower_left_corner[None]", self.cam_lower_left_corner)
#         print("u", u)
#         print("self.cam_horizontal[None]", u * self.cam_horizontal)
#         print("self.cam_vertical[None]", v * self.cam_vertical)
#         print("self.cam_origin[None]", self.cam_origin)
        
        return direction
    
    def get_impossible_intersection(self,index,u,v):
        direction = self.get_direction(u,v)
        return self.lookfrom + index*direction