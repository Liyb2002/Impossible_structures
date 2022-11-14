import structure
import numpy as np

seed = np.array([[0.0,0.0,.00], [0.0,0.1,0.0],[0.0,0.2,0.0],[0.0,0.3,0.0], [0.0,0.4,0.0]])
seed_next_possible = np.array([[-0.1,0.4,0.0,0],[0.1,0.4,0.0,1]])

s = structure.Structure(seed, seed_next_possible)

s.generate(5)

for i in s.rect:
    i.info()