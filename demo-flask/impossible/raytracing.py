import numpy as np


class ortho_camera:
    def __init__(self):
        # Define the camera parameters
        self.camera_position = np.array([5.0, 5.0, 5.0])  # Camera position in 3D space
        self.lookat_point = np.array([0.0, 0.0, 0.0])   # Look-at point (where the camera is pointing)
        self.up_vector = np.array([0.0, 1.0, 0.0])       # Up vector for camera orientation
        self.screen_width = 800                    # Width of the screen in pixels
        self.screen_height = 800                   # Height of the screen in pixels
        self.world_width = 5.0                      # Width of the world coordinates
        self.world_height = (self.screen_height / self.screen_width) * self.world_width  # Height of the world coordinates

        # Calculate the direction vectors
        self.direction = self.lookat_point - self.camera_position
        self.direction /= np.linalg.norm(self.direction)
        self.right = np.cross(self.direction, self.up_vector)
        self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.direction)

    def get_ray(self, x,y):
        ndc_x = (2 * x / self.screen_width) - 1
        ndc_y = 1 - (2 * y / self.screen_height)

        # Calculate the world coordinates of the current pixel
        world_x = self.camera_position[0] + (ndc_x * self.world_width * 0.5 * self.right[0])
        world_y = self.camera_position[1] + (ndc_y * self.world_height * 0.5 * self.up[1])
        world_z = self.camera_position[2] 

        # Create the ray from the camera to the current pixel
        ray_origin = np.array([world_x, world_y, world_z])

        return ray_origin

    def get_intersections(self, startPos, k1, k2):
        ro = self.get_ray(startPos[0], startPos[1])
        print("ro", ro)

        print("rd", self.direction)
        pos_1 = ro + (k1 *0.25) * self.direction
        pos_2 = ro + (k2 *0.25) * self.direction

        return (pos_1, pos_2)

startPos = np.array([100, 700])

k1 = 8
k2 = 34
myCam = ortho_camera()
pos_1, pos_2 = myCam.get_intersections(startPos, k1, k2)
print("pos_1:", pos_1, "pos_2:", pos_2)
