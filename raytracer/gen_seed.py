import numpy as np

def get_seed(pos, block_size, portion,isFront):
    seed = pos

    if isFront:
        for i in range(1,5):
            tempt = np.array([pos[0],pos[1]+block_size*i,pos[2]])
            seed = np.vstack([seed, tempt])
    else:
        for i in range(1,5):
            tempt = np.array([pos[0]-block_size*i * portion,pos[1],pos[2]])
            seed = np.vstack([seed, tempt])
    return seed


def get_next_possible(pos, block_size):
    tempt1 = np.array([pos[0],pos[1]+block_size,pos[2],3])
    tempt2 = np.array([pos[0],pos[1]-block_size,pos[2],2])
    
    return np.vstack([tempt1, tempt2])