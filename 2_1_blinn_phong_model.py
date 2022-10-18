import taichi as ti
import numpy as np
import argparse
import random

from ray_tracing_models import Ray, Camera, Hittable_list, Sphere, PI, xy_rect, xz_rect, yz_rect
ti.init(arch=ti.gpu)

PI = 3.14159265

# Canvas
aspect_ratio = 1.0
image_width = 800
image_height = int(image_width / aspect_ratio)
canvas = ti.Vector.field(3, dtype=ti.f32, shape=(image_width, image_height))
light_source = ti.Vector([0, 5.4 - 3.0, -1])

possible_intersects = ti.Vector.field(3, dtype=ti.f32, shape=(25))
# Rendering parameters
max_depth = 10

x_start = 500
y_start = 500

@ti.kernel
def get_impossible_intersection():
    for i, j in canvas:
        if i==x_start and j==y_start:
            u = (i) / image_width
            v = (j) / image_height
            ray = camera.get_ray(u, v)
            for k in range(5,25):
                x = ray.origin[0] + ray.direction[0] * (k*0.25)
                y = ray.origin[1] + ray.direction[1] * (k*0.25)
                z = ray.origin[2] + ray.direction[2] * (k*0.25)
                pos = ti.Vector([x, y,z])
                possible_intersects[k] += pos


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
    # Compute the local color use Blinn-Phong model
    hit_point_to_source = to_light_source(hit_point, light_source)
    # Diffuse light
    diffuse_color = color * ti.max(
        hit_point_to_source.dot(hit_point_normal) / (
                hit_point_to_source.norm() * hit_point_normal.norm()),
        0.0)
    diffuse_weight = 1.0
    if material != 1:
        # Specular light
        H = (-(ray_direction.normalized()) + hit_point_to_source.normalized()).normalized()
        N_dot_H = ti.max(H.dot(hit_point_normal.normalized()), 0.0)
        intensity = ti.pow(N_dot_H, 10)

    # Fuzz metal ball
    if material == 4:
        diffuse_weight = 0.5

    return diffuse_weight * diffuse_color

def create_rect(start_x, start_y, start_z, x_len, y_len, z_len):
    scene.add(xy_rect(_x0=start_x, _x1=start_x+x_len, _y0=start_y, _y1=start_y+y_len, _k=start_z, material=1, color=ti.Vector([0.3, 0.3, 0.8])))
    scene.add(xy_rect(_x0=start_x, _x1=start_x+x_len, _y0=start_y, _y1=start_y+y_len, _k=start_z+z_len, material=1, color=ti.Vector([0.3, 0.3, 0.8])))
    
    scene.add(xz_rect(_x0=start_x, _x1=start_x+x_len, _z0=start_z, _z1=start_z+z_len, _k=start_y, material=1, color=ti.Vector([0.2, 0.4, 0.5])))
    scene.add(xz_rect(_x0=start_x, _x1=start_x+x_len, _z0=start_z, _z1=start_z+z_len, _k=start_y+y_len, material=1, color=ti.Vector([0.2, 0.4, 0.5])))

    scene.add(yz_rect(_y0=start_y, _y1=start_y+y_len, _z0=start_z, _z1=start_z+z_len, _k=start_x, material=1, color=ti.Vector([0.3, 0.3, 0.2])))
    scene.add(yz_rect(_y0=start_y, _y1=start_y+y_len, _z0=start_z, _z1=start_z+z_len, _k=start_x+x_len, material=1, color=ti.Vector([0.3, 0.3, 0.2])))


# Blinn–Phong reflection model
@ti.func
def ray_color(ray):
    color_buffer = ti.Vector([1.0, 1.0, 1.0])
    curr_origin = ray.origin
    curr_direction = ray.direction
    is_hit, hit_point, hit_point_normal, front_face, material, color = scene.hit(Ray(curr_origin, curr_direction))
    if is_hit:
        if material == 0:
            color_buffer = color
        else:
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

    get_impossible_intersection()
    foreground_index = random.randint(5, 10)
    foreground_x = possible_intersects[foreground_index][0]
    foreground_y = possible_intersects[foreground_index][1]
    foreground_z = possible_intersects[foreground_index][2]


    background_index = random.randint(foreground_index, 15)
    background_x = possible_intersects[background_index][0]
    background_y = possible_intersects[background_index][1]
    background_z = possible_intersects[background_index][2]

    #render foreground
    create_rect(foreground_x, foreground_y, foreground_z, 0.5, 0.1, 0.1)
    create_rect(background_x, background_y, background_z, 0.1, 0.5, 0.1)

    #render background
    #scene.add(xy_rect(_x0=background_x, _x1=background_x + 0.1, _y0=background_y, _y1=background_y + 0.5, _k=background_z, material=1, color=ti.Vector([0.3, 0.3, 0.8])))
    #scene.add(xy_rect(_x0=background_x, _x1=background_x + 0.1, _y0=background_y, _y1=background_y + 0.5, _k=background_z + 0.1, material=1, color=ti.Vector([0.3, 0.3, 0.8])))


    while gui.running:
        render()
        cnt += 1
        gui.set_image(np.sqrt(canvas.to_numpy() / cnt))
        gui.show()