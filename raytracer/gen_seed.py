import numpy as np
import random

def get_seed(pos, block_size, portion,isFront):
    seed = pos
    intersect_type = random.randint(1,8)

    if isFront:
        if intersect_type == 1:
            for i in range(1,5):
                tempt = np.array([pos[0],pos[1]+block_size*i,pos[2]])
                seed = np.vstack([seed, tempt])
        
        elif intersect_type == 2:
            for i in range(1,5):
                tempt = np.array([pos[0],pos[1]-block_size*i,pos[2]])
                seed = np.vstack([seed, tempt])
        
        elif intersect_type == 3 or intersect_type == 4:
            for i in range(1,5):
                tempt = np.array([pos[0]+block_size*i,pos[1],pos[2]])
                seed = np.vstack([seed, tempt])
        


    else:
        if intersect_type == 1 or intersect_type == 2:
            for i in range(1,5):
                tempt = np.array([pos[0]-block_size*i * portion,pos[1],pos[2]])
                seed = np.vstack([seed, tempt])
        
        elif intersect_type == 3:
            for i in range(1,5):
                tempt = np.array([pos[0],pos[1]-block_size*i * portion,pos[2]])
                seed = np.vstack([seed, tempt])
        
        elif intersect_type == 4:
            for i in range(1,5):
                tempt = np.array([pos[0]-block_size * portion,pos[1]+block_size*i * portion,pos[2]])
                seed = np.vstack([seed, tempt])

        

    return seed


def get_next_possible(pos, block_size):
    tempt1 = np.array([pos[0],pos[1]+block_size,pos[2],3])
    tempt2 = np.array([pos[0],pos[1]-block_size,pos[2],2])
    
    return np.vstack([tempt1, tempt2])