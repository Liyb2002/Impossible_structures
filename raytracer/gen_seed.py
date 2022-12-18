import numpy as np

def get_seed(pos, block_size, portion, isFront, type):
    seed = pos
    seed_len = int(5 * 0.05/block_size )
    if isFront:
        if type == 1:
            for i in range(0,seed_len):
                tempt = np.array([pos[0],pos[1]+block_size*i*portion,pos[2]])
                seed = np.vstack([seed, tempt])
        
        if type == 2:
            for i in range(0,seed_len):
                tempt = np.array([pos[0]+block_size*i*portion,pos[1],pos[2]])
                seed = np.vstack([seed, tempt])

        if type == 3:
            for i in range(0,seed_len):
                tempt = np.array([pos[0],pos[1]+block_size*i*portion,pos[2]])
                seed = np.vstack([seed, tempt])
                
        
    else:
        if type == 1:
            for i in range(0,seed_len):
                tempt = np.array([pos[0]-block_size*i * portion,pos[1],pos[2]])
                seed = np.vstack([seed, tempt])
        
        if type == 2:
            for i in range(0,seed_len):
                tempt = np.array([pos[0],pos[1]-block_size*i * portion,pos[2]])
                seed = np.vstack([seed, tempt])

        if type == 3:
            for i in range(0,seed_len):
                tempt = np.array([pos[0],pos[1]-block_size*i * portion,pos[2]])
                seed = np.vstack([seed, tempt])
                
        
    return seed


def get_next_possible(pos, block_size, isFront, type):

    if isFront:
        if type == 1 or type == 3:
            tempt1 = np.array([pos[0],pos[1]+block_size,pos[2],3])
            tempt2 = np.array([pos[0],pos[1]-block_size,pos[2],2])
        
        if type == 2:
            tempt1 = np.array([pos[0]+block_size,pos[1],pos[2],1])
            tempt2 = np.array([pos[0]-block_size,pos[1],pos[2],0])

    else:
        if type == 1:
            tempt1 = np.array([pos[0]+block_size,pos[1],pos[2],1])
            tempt2 = np.array([pos[0]-block_size,pos[1],pos[2],0])
        
        if type == 2 or type == 3:
            tempt1 = np.array([pos[0],pos[1]+block_size,pos[2],1])
            tempt2 = np.array([pos[0],pos[1]-block_size,pos[2],0])

    return np.vstack([tempt1, tempt2])