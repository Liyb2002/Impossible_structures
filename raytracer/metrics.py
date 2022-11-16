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