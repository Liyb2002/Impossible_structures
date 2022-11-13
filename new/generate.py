#import visualize
import structure
import numpy as np

if __name__ == '__main__':
    seed = np.array([[0,0,0], [0,1,0],[0,2,0],[0,3,0], [0,4,0]])
    seed_next_possible = np.array([[-1,4,0,0],[1,4,0,1]])

    myStructure = structure.Structure(seed, seed_next_possible)

    myStructure.generate(5)