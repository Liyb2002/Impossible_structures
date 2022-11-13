from scene import Scene
import taichi as ti
from taichi.math import *
import numpy as np

ti.init(arch=ti.gpu)


PI = 3.14159265
scene = Scene(exposure=1)
scene.set_directional_light((0, 1, 1), 0.1, (1, 1, 1))
scene.set_background_color((0.3, 0.4, 0.6))



@ti.kernel
def initialize_voxels(pos: vec3):
    scene.set_voxel(pos, 1, vec3(0.5, 0.5, 0.5))


def run(voxels):
    for i in range(2):
        initialize_voxels(vec3(voxels[i][0] , voxels[i][1] , voxels[i][2]))


scene.finish()