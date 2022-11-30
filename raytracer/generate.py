import taichi as ti
import numpy as np
import argparse
import random
import json

import structure
import gen_seed
import connecting_comp
import metrics
import intersection
import particle

ti.init(arch=ti.gpu)

PI = 3.14159265

# Canvas
aspect_ratio = 1.0
image_width = 800
image_height = int(image_width / aspect_ratio)
canvas = ti.Vector.field(3, dtype=ti.f32, shape=(image_width, image_height))


if __name__ == "__main__":

    gui = ti.GUI("Ray Tracing", res=(image_width, image_height))
    canvas.fill(0)
    cnt = 0

    num_connections = 0
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        num_layers = config_data[0]['num_layers']
        num_connections = config_data[0]['num_connections']
        block_size = config_data[0]['block_size']


    max_score = -1000
    result_particle = None

    foreground_index = 8
    background_index = 12
    dummy_index = 17

    basic_scene = intersection.Scene()
    foreground_max_screen = basic_scene.get_max_screen(foreground_index)
    background_max_screen = basic_scene.get_max_screen(background_index)    
    dummy_max_screen = basic_scene.get_max_screen(dummy_index)

    foreground_min_screen = basic_scene.get_min_screen(foreground_index)
    background_min_screen = basic_scene.get_min_screen(background_index)
    dummy_min_screen = basic_scene.get_min_screen(dummy_index)

    foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
    background_intersection = basic_scene.get_possible_intersects(background_index)
    dummy_intersection = basic_scene.get_possible_intersects(dummy_index)
    offset_x = connecting_comp.offset()
    offset_y = connecting_comp.offset()

    dummy_intersection = np.array([dummy_intersection[0]+offset_x, dummy_intersection[1]+offset_y, dummy_intersection[2]])

    portion = background_index/ foreground_index

    num_particles = 300
    steps = 0
    particle_list = []
    score_list = []


    #initialize particles
    for i in range(num_particles):
        tempt_particle = particle.Particle(foreground_max_screen,background_max_screen,foreground_min_screen,background_min_screen, foreground_intersection, background_intersection, portion, 1, block_size)
        tempt_particle.generate_dummy_comp(dummy_max_screen, dummy_min_screen, dummy_intersection, portion, num_connections-1)
        tempt_score = tempt_particle.total_score()
        particle_list.append(tempt_particle)
        score_list.append(tempt_score)

    particle_list = particle.resample(particle_list, score_list)

    #generate and resampling
    for s in range(steps):
        score_list = []
        for i in range(len(particle_list)):
            particle_list[i].generate_one()
            score_list.append(particle_list[i].total_score())
        
        print("size of particle list: ", len(particle_list), "size of score list: ", len(score_list))
        particle_list = particle.resample(particle_list, score_list)
    
    print("finishing process")
    # finish the process
    for i in range (len(particle_list)):
        particle_list[i].finish()
        score_list[i] = particle_list[i].total_score()
    
    particle_list = particle.resample(particle_list, score_list)
    result_particle = particle_list[0]

    #create a json file, and write the result
    with open('../three/result.json', 'w') as f:
        result = []
        for cc in result_particle.connecting_comp:
            i = cc.get_object()
            data = {'obj':
                {'start_x': i.start_x, 
                'start_y': i.start_y, 
                'start_z': i.start_z, 
                'scale_x': i.scale_x, 
                'scale_y': i.scale_y, 
                'scale_z': i.scale_z}
            }
            result.append(data)
        
        f_struct = result_particle.foreground_structure
        b_struct = result_particle.background_structure
        d_struct = result_particle.dummy_structure

        for i in f_struct.rect:
            data = {'obj':
                {'start_x': i.start_x, 
                'start_y': i.start_y, 
                'start_z': i.start_z, 
                'scale_x': i.scale_x, 
                'scale_y': i.scale_y, 
                'scale_z': i.scale_z}
            }
            result.append(data)

        for i in b_struct.rect:
            data = {'obj':
                {'start_x': i.start_x, 
                'start_y': i.start_y, 
                'start_z': i.start_z, 
                'scale_x': i.scale_x, 
                'scale_y': i.scale_y, 
                'scale_z': i.scale_z}
            }
            result.append(data)
        
        if d_struct != None:
            for i in d_struct.rect:
                data = {'obj':
                    {'start_x': i.start_x, 
                    'start_y': i.start_y, 
                    'start_z': i.start_z, 
                    'scale_x': i.scale_x, 
                    'scale_y': i.scale_y, 
                    'scale_z': i.scale_z}
                }
                result.append(data)

        json.dump(result, f, indent=2)


