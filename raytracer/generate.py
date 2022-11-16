import taichi as ti
import numpy as np
import argparse
import random

import structure
import gen_seed
import connecting_comp
import metrics
import intersection
import particle

from ray_tracing_models import Ray, Camera, Hittable_list, PI, xy_rect, xz_rect, yz_rect
ti.init(arch=ti.gpu)

PI = 3.14159265

# Canvas
aspect_ratio = 1.0
image_width = 800
image_height = int(image_width / aspect_ratio)
canvas = ti.Vector.field(3, dtype=ti.f32, shape=(image_width, image_height))
light_source = ti.Vector([0, 5.4 - 3.0, -1])

# Rendering parameters
max_depth = 10

@ti.kernel
def render():
    for i, j in canvas:
        u = (i) / image_width
        v = (j) / image_height
        color = ti.Vector([0.0, 0.0, 0.0])
        ray = camera.get_ray(u, v)
        color += ray_color(ray)
        canvas[i, j] += color

@ti.func
def to_light_source(hit_point, light_source):
    return light_source - hit_point


@ti.func
def blinn_phong(ray_direction, hit_point, hit_point_normal, color, material):

    hit_point_to_source = to_light_source(hit_point, light_source)
    # Diffuse light
    diffuse_color = color * ti.max(
        hit_point_to_source.dot(hit_point_normal) / (
                hit_point_to_source.norm() * hit_point_normal.norm()),
        0.0)

    return diffuse_color

def create_rect(start_x, start_y, start_z, x_len, y_len, z_len,r,g,b):
    # scene.add(xy_rect(_x0=start_x, _x1=start_x+x_len, _y0=start_y, _y1=start_y+y_len, _k=start_z, material=1, color=ti.Vector([r, g, b])))
    scene.add(xy_rect(_x0=start_x, _x1=start_x+x_len, _y0=start_y, _y1=start_y+y_len, _k=start_z+z_len, material=1, color=ti.Vector([r, g, b])))
    
    # scene.add(xz_rect(_x0=start_x, _x1=start_x+x_len, _z0=start_z, _z1=start_z+z_len, _k=start_y, material=1, color=ti.Vector([0.2, 0.4, 0.5])))
    scene.add(xz_rect(_x0=start_x, _x1=start_x+x_len, _z0=start_z, _z1=start_z+z_len, _k=start_y+y_len, material=1, color=ti.Vector([0.8, 0.8, 0.5])))

    # scene.add(yz_rect(_y0=start_y, _y1=start_y+y_len, _z0=start_z, _z1=start_z+z_len, _k=start_x, material=1, color=ti.Vector([0.3, 0.3, 0.2])))
    scene.add(yz_rect(_y0=start_y, _y1=start_y+y_len, _z0=start_z, _z1=start_z+z_len, _k=start_x+x_len, material=1, color=ti.Vector([0.3, 0.3, 0.9])))

# Blinn–Phong reflection model
@ti.func
def ray_color(ray):
    color_buffer = ti.Vector([1.0, 1.0, 1.0])
    curr_origin = ray.origin
    curr_direction = ray.direction
    is_hit, hit_point, hit_point_normal, front_face, material, color = scene.hit(Ray(curr_origin, curr_direction))
    if is_hit:
        color_buffer = blinn_phong(curr_direction, hit_point, hit_point_normal, color, material)
    return color_buffer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Naive Ray Tracing')
    parser.add_argument(
        '--max_depth', type=int, default=10, help='max depth (default: 10)')
    parser.add_argument(
        '--samples_per_pixel', type=int, default=4, help='samples_per_pixel  (default: 4)')
    args = parser.parse_args()

    max_depth = args.max_depth
    samples_per_pixel = args.samples_per_pixel
    scene = Hittable_list()

    camera = Camera()
    gui = ti.GUI("Ray Tracing", res=(image_width, image_height))
    canvas.fill(0)
    cnt = 0

    particle = particle.Particle()

    cc = particle.connecting_comp
    i = cc.get_object()
    create_rect(i.start_x, i.start_y, i.start_z, i.scale_x, i.scale_y, i.scale_z, 0.2, 0.4, 0.5)

    f_struct = particle.foreground_structure
    for i in f_struct.rect:
        create_rect(i.start_x, i.start_y, i.start_z, i.scale_x, i.scale_y, i.scale_z, 0.2, 0.4, 0.5)
    
    b_struct = particle.background_structure
    for i in b_struct.rect:
        create_rect(i.start_x, i.start_y, i.start_z, i.scale_x, i.scale_y, i.scale_z, 0.9, 0.2, 0.3)

    # eye = np.array([5.0,5.0,5.0])
    # pos = cc.get_center()
    # occluded = metrics.occlude(f_struct, pos, eye)
    # if(occluded):
    #     print("occluded")
    # else:
    #     print("not occluded")

    # #off screen
    # foreground_max_screen = intersections.get_max_screen(foreground_index)
    # background_max_screen = intersections.get_max_screen(background_index)
    # foreground_min_screen = intersections.get_min_screen(foreground_index)
    # background_min_screen = intersections.get_min_screen(background_index)

    # foreground_out_of_screen = metrics.out_of_screen(f_struct, foreground_max_screen, foreground_min_screen)
    # print("foreground out of screen: ", foreground_out_of_screen)
    # (score, parallel_pts) = structure.parallel_score(np.round(f_struct.history,1), np.round(b_struct.history,1))


    while gui.running:
        render()
        cnt += 1
        gui.set_image(np.sqrt(canvas.to_numpy() / cnt))
        gui.show()