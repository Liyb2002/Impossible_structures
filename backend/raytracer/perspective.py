import math
import numpy as np

# initialize camera parameters
camera_pos = np.array([5, 5, 5])
lookAt = np.array([0, 0, 0])
up = np.array([0, 0, 1])
look_vec = lookAt - camera_pos

w = 800
h = 800
near = 0.1
far = 100

theta_w = 45
theta_w = math.radians(theta_w)

theta_h = 45
theta_h = math.radians(theta_h)

c = -near / far


def get_m_view():
    look_vec = lookAt - camera_pos
    w = -look_vec / np.linalg.norm(look_vec)
    v = up - np.dot(up, w) * w
    v = v / np.linalg.norm(v)
    u = np.cross(v, w)

    m_rotate = np.array(
        [
            [u[0], u[1], u[2], 0],
            [v[0], v[1], v[2], 0],
            [w[0], w[1], w[2], 0],
            [0, 0, 0, 1],
        ]
    )

    m_view = np.array(
        [
            [m_rotate[0][0], m_rotate[0][1], m_rotate[0][2], camera_pos[0]],
            [m_rotate[1][0], m_rotate[1][1], m_rotate[1][2], camera_pos[1]],
            [m_rotate[2][0], m_rotate[2][1], m_rotate[2][2], camera_pos[2]],
            [0, 0, 0, 1],
        ]
    )

    return np.around(m_view, 2)


def get_m_proj():
    m_proj = np.array(
        [
            [1 / (math.tan(theta_w / 2)), 0, 0, 0],
            [0, 1 / (math.tan(theta_h / 2)), 0, 0],
            [0, 0, c, -1],
            [0, 0, c * near, 0],
        ]
    )
    return m_proj


import math

PI = 3.14


class Camera:
    def __init__(self, fov=60, aspect_ratio=1.0):
        # Camera parameters
        self.lookfrom = np.array([5.0, 5.0, 5.0])
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

        self.cam_lower_left_corner = (
            self.cam_origin - half_width * u - half_height * v - w
        )
        self.cam_horizontal = 2 * half_width * u
        self.cam_vertical = 2 * half_height * v

    def get_ray(self, u, v):
        r = (
            self.cam_lower_left_corner
            + u * self.cam_horizontal
            + v * self.cam_vertical
            - self.cam_origin
        )
        return r

    def get_camera_origin(self):
        return self.cam_origin
