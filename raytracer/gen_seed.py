import numpy as np

def get_seed(pos):
    seed = pos
    for i in range(1,5):
        tempt = np.array([pos[0],pos[1]+0.07*i,pos[2]])
        seed = np.vstack([seed, tempt])
    return seed

def get_seed_2(pos, portion):
    seed = pos
    for i in range(1,5):
        tempt = np.array([pos[0]-0.07*i * portion,pos[1],pos[2]])
        seed = np.vstack([seed, tempt])
    return seed


def get_next_possible(pos):
    tempt1 = np.array([pos[0],pos[1]+0.07,pos[2],2])
    tempt2 = np.array([pos[0],pos[1]-0.07,pos[2],3])
    
    return np.vstack([tempt1, tempt2])