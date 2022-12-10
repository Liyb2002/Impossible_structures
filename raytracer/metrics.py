import numpy as np
import perspective
import rasterizer

from sympy import *
x, y, z = symbols('x y z')

m_view = perspective.get_m_view()
m_proj = perspective.get_m_proj()

def parallel_score(history_a, history_b):
    score = 0
    parallel_pts = []
    
    for i in history_a:
        for j in history_b:
            if(i[0] == j[0] and i[1] == j[1]):
                parallel_pts.append((i[0],i[1]))
                score += 5
            elif(i[0] == j[0] or i[1] == j[1]):
                score += 1
    return score, parallel_pts

def occlude(front_structure,position, eye):
    ray = eye - position
    ray = ray / np.linalg.norm(ray)
    # print("ray", ray)

    z_depth = front_structure.history[0][-1]
    t = (front_structure.seed[0][-1] - position[-1]) / ray[-1]
    # print("t", t)

    x = position[0] + t*ray[0]
    y = position[1] + t*ray[1]
    z = position[2] + t*ray[2]
    # print("x", x, "y", y, "z", z)
    
    for i in front_structure.history:

        if x > i[0] and x < i[0] + 0.07 and y > i[1] and y < i[1] + 0.07:
            return True
        
        if x < i[0] and x > i[0] - 0.07 and y < i[1] and y > i[1] - 0.07:
            return True
    
    return False

def occlusion_score(front_structure, points, eye):
    count = 0
    for i in points:
        if (occlude(front_structure, i, eye)):
            count += 1
    
    return count

def occlusion_score_wDist(front_structure, points, eye, axis, start, end):
    score = 0
    for i in points:
        if (occlude(front_structure, i, eye)):
            dist = min(abs(start - i[axis]), abs(end-i[axis]))
            score += dist * -5 
    
    return score

def occlusion_score_structures(front_structure, back_structure, eye):

    total_score = 0

    for i in back_structure.rect:
        x_scale = i.scale_x
        y_scale = i.scale_y
        z_scale = i.scale_z
        dist = max(x_scale, y_scale, z_scale)

        scale_vec = np.array([x_scale, y_scale, z_scale])
        dir = np.argmax(scale_vec)

        if(dir == 0):
            start = i.start_x
            end = i.start_x + x_scale
        
        elif(dir == 1):
            start = i.start_y
            end = i.start_y + y_scale
        
        else:
            start = i.start_z
            end = i.start_z + z_scale
        
        step = 0.05
        points_list = []

        while step < dist:
            if(dir == 0):
                points_list.append((start + step, i.start_y, i.start_z))
            elif(dir == 1):
                points_list.append((i.start_x, start + step, i.start_z))
            else:
                points_list.append((i.start_x, i.start_y, start + step))
            step += 0.05
        
        score = occlusion_score_wDist(front_structure, points_list, eye, dir, start, end)
        # print("score", score)
        total_score += score
    
    # print("total_score", total_score)
    return total_score


def occlusion_raster(front_structure, back_structure):
    score = 0
    mid_points = []
    for i in back_structure.rect:
        point = np.array([i.start_x + i.scale_x/2, i.start_y + i.scale_y/2, i.start_z + i.scale_z/2, 1])
        mid_points.append(point)
    
    graph_back = rasterizer.get_graph(back_structure.rect)

    for rect in front_structure.rect:
        start_x = rect.start_x
        start_y = rect.start_y
        start_z = rect.start_z
        scale_x = rect.scale_x
        scale_y = rect.scale_y

        m_view = perspective.get_m_view()
        m_proj = perspective.get_m_proj()

        right_up = np.array([start_x + scale_x, start_y + scale_y, start_z, 1])
        left_down = np.array([start_x, start_y, start_z, 1])

        right_up = right_up.dot(m_view).dot(m_proj)
        left_down = left_down.dot(m_view).dot(m_proj)

        right_up_x = int(to_pixel_x(right_up[0]))
        right_up_y = int(to_pixel_y(right_up[1]))
        left_down_x = int(to_pixel_x(left_down[0]))
        left_down_y = int(to_pixel_y(left_down[1]))

        for i in range(left_down_x, right_up_x):
            for j in range(left_down_y, right_up_y):
                if(graph_back[i][j] == 1):
                    x = start_x + (i - left_down_x) * scale_x / (right_up_x - left_down_x)
                    y = start_y + (j - left_down_y) * scale_y / (right_up_y - left_down_y)
                    dist = 1000
                    for k in mid_points:
                        if(dist > math.sqrt((x-k[0])**2 + (y-k[1])**2)):
                            dist = math.sqrt((x-k[0])**2 + (y-k[1])**2)
                    
                    score += np.log(dist+1)

    return score


def out_of_screen(structure, max_coordinate, min_coordinate):

    if structure == None:
        return False
    
    max_x = max_coordinate[0]
    max_y = max_coordinate[1]
    min_x = min_coordinate[0]
    min_y = min_coordinate[1]
    
    for i in structure.rect:
        if(i.start_x < min_x or i.start_y < min_y):
            return True
        if(i.start_x+i.scale_x > max_x or i.start_y+i.scale_y > max_y):
            return True
    
    return False

def too_close(structure):

    if structure == None:
        return False

    horizontal = []
    vertical = []

    for i in structure.rect:
        if(i.scale_x > i.scale_y):
            horizontal.append(i)
        else:
            vertical.append(i)
    
    for i in horizontal:
        for j in horizontal:
            if(i.start_y != j.start_y and abs(i.start_y - j.start_y)<0.2):
                return True
    
    for i in vertical:
        for j in vertical:
            if(i.start_x != j.start_x and abs(i.start_x - j.start_x)<0.2):
                return True
    
    return False


def size_score(structure_a, struct_b):
    x_max = max(structure_a.max_x, struct_b.max_x)
    y_max = max(structure_a.max_y, struct_b.max_y)
    x_min = min(structure_a.min_x, struct_b.min_x)
    y_min = min(structure_a.min_y, struct_b.min_y)

    area = (x_max - x_min) * (y_max - y_min)

    return area

def to_pixel_x(x):
    return x*400 + 400

def to_pixel_y(y):
    return 400 - y*400
