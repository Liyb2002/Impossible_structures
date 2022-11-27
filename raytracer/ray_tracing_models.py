import taichi as ti

PI = 3.14159265
light_source = ti.Vector([0, 5.4 - 3.0, -1])

@ti.func
def to_light_source(hit_point, light_source):
    return light_source - hit_point


@ti.func
def diffuse(ray_direction, hit_point, hit_point_normal, color, material):

    hit_point_to_source = to_light_source(hit_point, light_source)
    # Diffuse light
    diffuse_color = color * ti.max(
        hit_point_to_source.dot(hit_point_normal) / (
                hit_point_to_source.norm() * hit_point_normal.norm()),
        0.0)

    return diffuse_color

@ti.data_oriented
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    
    @ti.func
    def at(self, t):
        return self.origin + t * self.direction

@ti.data_oriented
class xy_rect:
    def __init__(self, _x0, _x1, _y0, _y1, _k, color):
        self.x0 = _x0
        self.x1 = _x1
        self.y0 = _y0
        self.y1 = _y1
        self.k = _k
        self.color = color


    #return the hit information
    @ti.func
    def hit(self, camera_pos, ray, t_min=0.001, t_max=10e8):
        is_hit = True
        frontface = True
        hit_point =  ti.Vector([0.0, 0.0, 0.0])
        hit_point_normal = ti.Vector([0.0, 0.0, -1.0])

        t = (self.k - camera_pos[2]) / ray[2]

        if t <0.001 or t>10e8:
            is_hit = False
        else: 
            x = camera_pos[0] + t * ray[0]
            y = camera_pos[1] + t * ray[1]
            if x < self.x0 or x> self.x1 or y<self.y0 or y > self.y1:
                is_hit = False
            else:
                hit_point = camera_pos + t * ray
                frontface = True
        root = t
        return is_hit, root, hit_point, hit_point_normal, frontface, 1, self.color

@ti.data_oriented
class xz_rect:
    def __init__(self, _x0, _x1, _z0, _z1, _k, color):
        self.x0 = _x0
        self.x1 = _x1
        self.z0 = _z0
        self.z1 = _z1
        self.k = _k
        self.color = color


    #return the hit information
    @ti.func
    def hit(self, camera_pos, ray, t_min=0.001, t_max=10e8):
        is_hit = True
        frontface = True
        hit_point =  ti.Vector([0.0, 0.0, 0.0])
        hit_point_normal = ti.Vector([0.0, -1.0, 0.0])

        t = (self.k - camera_pos[1]) / ray[1]

        if t <0.001 or t>10e8:
            is_hit = False
        else: 
            x = camera_pos[0] + t * ray[0]
            z = camera_pos[2] + t * ray[2]
            if x < self.x0 or x> self.x1 or z<self.z0 or z > self.z1:
                is_hit = False
            else:
                hit_point = camera_pos + t * ray
                frontface = True
        root = t
        return is_hit, root, hit_point, hit_point_normal, frontface, 1, self.color

@ti.data_oriented
class yz_rect:
    def __init__(self, _y0, _y1, _z0, _z1, _k, color):
        self.y0 = _y0
        self.y1 = _y1
        self.z0 = _z0
        self.z1 = _z1
        self.k = _k
        self.color = color


    #return the hit information
    @ti.func
    def hit(self, camera_pos, ray, t_min=0.001, t_max=10e8):
        is_hit = True
        frontface = True
        hit_point =  ti.Vector([0.0, 0.0, 0.0])
        hit_point_normal = ti.Vector([-1.0, 0.0, 0.0])

        t = (self.k - camera_pos[0]) / ray[0]

        if t <0.001 or t>10e8:
            is_hit = False
        else: 
            y = camera_pos[1] + t * ray[1]
            z = camera_pos[2] + t * ray[2]
            if y < self.y0 or y> self.y1 or z<self.z0 or z > self.z1:
                is_hit = False
            else:
                hit_point = camera_pos + t * ray
                frontface = True
        root = t    
        return is_hit, root, hit_point, hit_point_normal, frontface, 1, self.color

@ti.data_oriented
class Hittable_list:
    def __init__(self):
        self.objects = []
    def add(self, obj):
        self.objects.append(obj)
    def clear(self):
        self.objects = []

    @ti.func
    def hit(self, camera_pos, ray, t_min=0.001, t_max=10e8):
        closest_t = t_max
        is_hit = False
        front_face = False
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_point_normal = ti.Vector([0.0, 0.0, 0.0])
        color = ti.Vector([0.0, 0.0, 0.0])
        material = 1
        for index in ti.static(range(len(self.objects))):
            is_hit_tmp, root_tmp, hit_point_tmp, hit_point_normal_tmp, front_face_tmp, material_tmp, color_tmp =  self.objects[index].hit(camera_pos, ray, t_min, closest_t)
            if is_hit_tmp and closest_t > root_tmp:
                closest_t = root_tmp
                is_hit = is_hit_tmp
                hit_point = hit_point_tmp
                hit_point_normal = hit_point_normal_tmp
                front_face = front_face_tmp
                material = material_tmp
                color = color_tmp
        return is_hit, hit_point, hit_point_normal, front_face, material, color


@ti.data_oriented
class Camera:
    def __init__(self, fov=60, aspect_ratio=1.0):
        # Camera parameters
        self.lookfrom = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.lookat = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.vup = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.fov = fov
        self.aspect_ratio = aspect_ratio

        self.cam_lower_left_corner = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.cam_horizontal = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.cam_vertical = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.cam_origin = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.reset()

    @ti.kernel
    def reset(self):
        self.lookfrom[None] = [5.0, 5.0, 5.0]
        self.lookat[None] = [0.0, 0.0, -1.0]
        self.vup[None] = [0.0, 1.0, 0.0]
        theta = self.fov * (PI / 180.0)
        half_height = ti.tan(theta / 2.0)
        half_width = self.aspect_ratio * half_height
        self.cam_origin[None] = self.lookfrom[None]
        w = (self.lookfrom[None] - self.lookat[None]).normalized()
        u = (self.vup[None].cross(w)).normalized()
        v = w.cross(u)
        self.cam_lower_left_corner[
            None] = self.cam_origin[None] - half_width * u - half_height * v - w
        self.cam_horizontal[None] = 2 * half_width * u
        self.cam_vertical[None] = 2 * half_height * v

    @ti.func
    def get_ray(self, u, v):
        r = self.cam_lower_left_corner[None] + u * self.cam_horizontal[None] + v * self.cam_vertical[None] - self.cam_origin[None]
        return r
    
    @ti.func
    def get_camera_origin(self):
        return self.cam_origin[None]