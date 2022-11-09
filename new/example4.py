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
def initialize_voxels():
    scene.set_voxel(vec3( -0.1916478 ,  0.20627433, -0.95823902), 1, vec3(0.9, 0.3, 0.3))
    scene.set_voxel(vec3( -0.1916478 ,  1.20627433, -0.95823902), 1, vec3(0.9, 0.3, 0.3))
    scene.set_voxel(vec3( -0.1916478 ,  2.20627433, -0.95823902), 1, vec3(0.9, 0.3, 0.3))
    scene.set_voxel(vec3( -0.1916478 ,  3.20627433, -0.95823902), 1, vec3(0.9, 0.3, 0.3))



    scene.set_voxel(vec3(-1.38886374,  0.10836577, -1.94431869), 1, vec3(0.9, 0.3, 0.3))
    scene.set_voxel(vec3(-2.38886374,  0.10836577, -1.94431869), 1, vec3(0.9, 0.3, 0.3))
    scene.set_voxel(vec3(-3.38886374,  0.10836577, -1.94431869), 1, vec3(0.9, 0.3, 0.3))




initialize_voxels()
scene.finish()
