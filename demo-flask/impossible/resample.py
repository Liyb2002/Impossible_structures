from copy import deepcopy
import numpy as np

def resample_particles(particle_list, score_list):
    total_score = sum(score_list)
    probabilities = [score / total_score for score in score_list]

    resampled_indices = np.random.choice(len(particle_list), size=len(particle_list), p=probabilities)

    new_particle_list = [deepcopy(particle_list[i]) for i in resampled_indices]

    return new_particle_list
