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
import perspective

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
        num_intersection = config_data[0]['num_intersection']
        connection = config_data[0]['connection']
        layer_index = config_data[0]['layer_index']
        num_connections = config_data[0]['num_connections']
        intersection_pos = config_data[0]['intersection_pos']
        block_size = config_data[0]['block_size']
        beam_mean = config_data[0]['beam_mean']
        beam_sd = config_data[0]['beam_sd']
        num_blocks_per_layer = config_data[0]['num_blocks_per_layer']
        num_particles = config_data[0]['num_particles']

    connecting_cost = beam_mean * 2 * num_connections

    max_score = -1000
    result_particle = None

    foreground_index = int(layer_index[0])
    background_index = int(layer_index[1])
    startPos = np.array([intersection_pos[0][0], intersection_pos[0][1]])
    basic_scene = intersection.Scene(startPos)

    foreground_intersection = basic_scene.get_possible_intersects(foreground_index)
    background_intersection = basic_scene.get_possible_intersects(background_index)
    portion = background_index/ foreground_index

    extra_foreground_intersection = []
    extra_background_intersection = []
    extra_backPortion = []

    for i in range(num_intersection-1):
        e_foreground_index = int(layer_index[2 * (i+1)])
        e_background_index = int(layer_index[2 * (i+1) + 1])
        dforeground_intersection = basic_scene.get_possible_intersects(e_foreground_index)
        dbackground_intersection = basic_scene.get_possible_intersects(e_background_index)
        e_startPos = np.array([intersection_pos[1][0], intersection_pos[1][1]])
        e_foreground_intersection = basic_scene.get_intersection_t(e_startPos, dforeground_intersection)
        e_background_intersection = basic_scene.get_intersection_t(e_startPos, dbackground_intersection)
        back_portion = e_background_index/ e_foreground_index
        extra_foreground_intersection.append(e_foreground_intersection)
        extra_background_intersection.append(e_background_intersection)
        extra_backPortion.append(back_portion)


    particle_list = []
    score_list = []
    #initialize particles
    for i in range(num_particles):
        tempt_particle = particle.Particle(foreground_intersection, background_intersection, portion, num_connections, block_size)
        tempt_particle.generate_structures()
        
        for j in range(num_intersection-1):
            tempt_particle.set_intersections(extra_foreground_intersection[j], extra_background_intersection[j], 1.0, extra_backPortion[j])
        
        tempt_particle.get_connecting_comp(connection)
        tempt_score = tempt_particle.total_score()
        particle_list.append(tempt_particle)
        score_list.append(tempt_score)

    particle_list = particle.resample(particle_list, score_list)

    steps = max(0, int((num_blocks_per_layer[1] - connecting_cost) / beam_mean))
    print("extra beams for background", steps)
    #generate background structure
    for s in range(steps):
        score_list = []
        for i in range(len(particle_list)):
            particle_list[i].structures[2].generate(1, beam_mean, beam_sd)
            score_list.append(particle_list[i].total_score())
        
        particle_list = particle.resample(particle_list, score_list)
    
    steps = int((num_blocks_per_layer[0] - connecting_cost) / beam_mean)
    print("extra beams for foreground", steps)
    #generate foreground structure
    for s in range(steps):
        score_list = []
        for i in range(len(particle_list)):
            particle_list[i].structures[1].generate(1, beam_mean, beam_sd)
            score_list.append(particle_list[i].total_score())
        
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
        
        for structure in result_particle.structures:
            for i in structure.rect:
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


