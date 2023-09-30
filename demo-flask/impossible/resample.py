from copy import deepcopy

def resample_particles(particle_list, score_list):
    new_particle_list = []

    for particle in particle_list:
        if particle.get_score() > 0:
            new_particle_list.append(particle)
    
    target_add = len(particle_list) - len(new_particle_list)
    sorted_index = sorted(range(len(score_list)), key=lambda k: score_list[k])
    sorted_index.reverse()

    for i in range(target_add):
        add_index = sorted_index[i]
        new_particle_list.append(particle_list[add_index])


    return new_particle_list
