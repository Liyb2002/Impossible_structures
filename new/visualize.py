from scene import Scene
import taichi as ti
from taichi.math import *
import numpy as np
import structure


ti.init(arch=ti.gpu)


PI = 3.14159265
scene = Scene(exposure=1)
scene.set_directional_light((0, 1, 1), 0.1, (1, 1, 1))
scene.set_background_color((0.3, 0.4, 0.6))



@ti.kernel
def initialize_voxels(pos: vec3):
    scene.set_voxel(pos, 1, vec3(0.5, 0.5, 0.5))


def run(voxels):
    for i in range(len(voxels)):
        initialize_voxels(vec3(voxels[i][0] , voxels[i][1] , voxels[i][2]))


seed = np.array([[0,0,0], [0,1,0],[0,2,0],[0,3,0], [0,4,0]])
seed_next_possible = np.array([[-1,4,0,0],[1,4,0,1]])

myStructure = structure.Structure(seed, seed_next_possible)

myStructure.generate(5)

gen_structure = myStructure.data

print(gen_structure)

run(gen_structure)

scene.finish()