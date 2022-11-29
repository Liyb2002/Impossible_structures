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

from ray_tracing_models import Camera, Hittable_list, PI, xy_rect, xz_rect, yz_rect, diffuse
ti.init(arch=ti.gpu)

PI = 3.14159265

# Canvas
aspect_ratio = 1.0
image_width = 800
image_height = int(image_width / aspect_ratio)
canvas = ti.Vector.field(3, dtype=ti.f32, shape=(image_width, image_height))

# Rendering parameters
max_depth = 10

@ti.kernel
def render():
    for i, j in canvas:
        u = (i) / image_width
        v = (j) / image_height
        color = ti.Vector([0.0, 0.0, 0.0])
        ray = camera.get_ray(u, v)
        camera_pos = camera.get_camera_origin()
        color += ray_color(ray, camera_pos)
        canvas[i, j] += color


def create_rect(start_x, start_y, start_z, x_len, y_len, z_len,r,g,b):
    # scene.add(xy_rect(_x0=start_x, _x1=start_x+x_len, _y0=start_y, _y1=start_y+y_len, _k=start_z, material=1, color=ti.Vector([r, g, b])))
    scene.add(xy_rect(_x0=start_x, _x1=start_x+x_len, _y0=start_y, _y1=start_y+y_len, _k=start_z+z_len, color=ti.Vector([r, g, b])))
    
    # # scene.add(xz_rect(_x0=start_x, _x1=start_x+x_len, _z0=start_z, _z1=start_z+z_len, _k=start_y, material=1, color=ti.Vector([0.2, 0.4, 0.5])))
    scene.add(xz_rect(_x0=start_x, _x1=start_x+x_len, _z0=start_z, _z1=start_z+z_len, _k=start_y+y_len, color=ti.Vector([0.8, 0.8, 0.5])))

    # # scene.add(yz_rect(_y0=start_y, _y1=start_y+y_len, _z0=start_z, _z1=start_z+z_len, _k=start_x, material=1, color=ti.Vector([0.3, 0.3, 0.2])))
    scene.add(yz_rect(_y0=start_y, _y1=start_y+y_len, _z0=start_z, _z1=start_z+z_len, _k=start_x+x_len, color=ti.Vector([0.3, 0.3, 0.9])))

@ti.func
def ray_color(ray, camera_pos):
    color_buffer = ti.Vector([1.0, 1.0, 1.0])
    curr_origin = camera_pos
    curr_direction = ray
    is_hit, hit_point, hit_point_normal, front_face, color = scene.hit(curr_origin, curr_direction)
    if is_hit:
        color_buffer = diffuse(curr_direction, hit_point, hit_point_normal, color)
    return color_buffer

if __name__ == "__main__":

    scene = Hittable_list()

    camera = Camera()
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
    steps = 1
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
    #finish the process
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


    # for cc in result_particle.connecting_comp:
    #     i = cc.get_object()
    #     create_rect(i.start_x, i.start_y, i.start_z, i.scale_x, i.scale_y, i.scale_z, 0.2, 0.4, 0.8)

    # f_struct = result_particle.foreground_structure
    # for i in f_struct.rect:
    #     create_rect(i.start_x, i.start_y, i.start_z, i.scale_x, i.scale_y, i.scale_z, 0.2, 0.4, 0.8)
    
    # b_struct = result_particle.background_structure
    # for i in b_struct.rect:
    #     create_rect(i.start_x, i.start_y, i.start_z, i.scale_x, i.scale_y, i.scale_z, 0.2, 0.9, 0.3)

    # d_struct = result_particle.dummy_structure
    # for i in d_struct.rect:
    #     create_rect(i.start_x, i.start_y, i.start_z, i.scale_x, i.scale_y, i.scale_z, 0.9, 0.1, 0.1)

    # while gui.running:
    #     render()
    #     cnt += 1
    #     gui.set_image(np.sqrt(canvas.to_numpy() / cnt))
    #     gui.show()