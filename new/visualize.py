from scene import Scene
import taichi as ti
from taichi.math import *
import numpy as np

import structure
import intersections


ti.init(arch=ti.gpu)

scene = Scene(exposure=1)
scene.set_floor(height=-50, color=(0.2, 0.2, 0.6))

scene.set_directional_light((0, 1, 1), 0.1, (1, 1, 1))
scene.set_background_color((0.3, 0.4, 0.6))


@ti.kernel
def initialize_voxels(pos: vec3):
    scene.set_voxel(pos, 1, vec3(0.5, 0.5, 0.5))


def run(voxels):
    for i in range(len(voxels)):
        initialize_voxels(vec3(voxels[i][0] , voxels[i][1] , voxels[i][2]))


myCamera = intersections.Camera()
foreground = myCamera.get_impossible_intersection(1.5,400, 500)
background = myCamera.get_impossible_intersection(2,400, 500)

forground_seed = np.array([(foreground[0],foreground[1]-1, foreground[2]),
            (foreground[0],foreground[1], foreground[2]), 
              (foreground[0],foreground[1]+1, foreground[2]),
            (foreground[0],foreground[1]+2, foreground[2])
               ])
forground_seed_last = forground_seed[-1]

forground_next_possible = np.array([
    (forground_seed_last[0],forground_seed_last[1]+1,forground_seed_last[2],3),
    (forground_seed_last[0]+1,forground_seed_last[1],forground_seed_last[2],1),
    (forground_seed_last[0]-1,forground_seed_last[1],forground_seed_last[2],0),
  
])

background_seed = np.array([
              (background[0]-1,background[1], background[2]),
                (background[0]-2,background[1], background[2]),
                (background[0]-3,background[1], background[2])
               ])

background_seed_last = background_seed[-1]

background_next_possible = np.array([
    (background_seed_last[0]-1,background_seed_last[1],background_seed_last[2],0),
    (background_seed_last[0],background_seed_last[1]+1,background_seed_last[2],2),
    (background_seed_last[0],background_seed_last[1]-1,background_seed_last[2],3),
])


myStructure_forground = structure.Structure(forground_seed, forground_next_possible)
myStructure_forground.generate(5)
gen_structure_forground = myStructure_forground.data


step = 1.0 / 64.0
real_pos = np.array([[0.0, 0.0, 0.0], [0.0, 0.2, 0.0]])

a = np.array([[-21.22272567, -36.03280631,   2.30698779]])
a_expand = np.array([a[0],
(a[0][0]+1,a[0][1],a[0][2]),
(a[0][0]+2,a[0][1],a[0][2])
        ])

b = np.array([[-19.78202642, -33.9394892 ,   3.22061894]])        
b_expand = np.array([(b[0][0],b[0][1]+1,b[0][2]),
(b[0][0],b[0][1] +2,b[0][2]),
(b[0][0],b[0][1] +3,b[0][2]), b[0]
        ])

run(b_expand)
run(a_expand)


#run(background_seed)

myStructure_background = structure.Structure(background_seed, background_next_possible)
myStructure_background.generate(5)
gen_structure_background = myStructure_background.data

#run(forground_seed)


scene.finish()