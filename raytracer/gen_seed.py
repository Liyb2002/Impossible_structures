import numpy as np
import random

def get_seed(pos, block_size, portion,isFront, intersect_type):
    seed = pos

    if isFront:
        if intersect_type == 1:
            for i in range(1,5):
                tempt = np.array([pos[0],pos[1]+block_size*i,pos[2]])
                seed = np.vstack([seed, tempt])
                
        elif intersect_type == 2:
            for i in range(1,5):
                tempt = np.array([pos[0],pos[1],pos[2]])
                seed = np.vstack([seed, tempt])
    else:
        if intersect_type == 1:
            for i in range(1,5):
                tempt = np.array([pos[0]-block_size*i * portion,pos[1],pos[2]])
                seed = np.vstack([seed, tempt])
        
        elif intersect_type == 2:
            for i in range(1,5):
                tempt = np.array([pos[0],pos[1]-block_size*i * portion,pos[2]])
                seed = np.vstack([seed, tempt])
        
        
    return seed


def get_next_possible(pos, block_size,isFront, intersect_type):

    if isFront:
        if intersect_type == 1:
            tempt1 = np.array([pos[0],pos[1]+block_size,pos[2],3])
        elif intersect_type == 2:
            tempt1 = np.array([pos[0]+block_size,pos[1],pos[2],1])

    else:
        if intersect_type == 1:
            tempt1 = np.array([pos[0]-block_size,pos[1],pos[2],0])
        elif intersect_type == 2:
            tempt1 = np.array([pos[0],pos[1]-block_size,pos[2],2])

    return np.vstack([tempt1])