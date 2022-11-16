import numpy as np

def occlude(front_structure,position, eye):
    ray = eye - position
    ray = ray / np.linalg.norm(ray)
#     print("ray", ray)

    z_depth = front_structure.history[0][-1]
    t = (eye[-1] - z_depth) / ray[-1]
#     print("t", t)

    x = eye[0] + t*ray[0]
    y = eye[1] + t*ray[1]
    
    for i in front_structure.history:
        if round(x,1)== round(i[0],1) and round(y,1) == round(i[1],1):
            return True
    
    return False

def out_of_screen(structure, max_coordinate, min_coordinate):
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