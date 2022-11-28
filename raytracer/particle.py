import numpy as np

import intersection
import structure
import connecting_comp
import gen_seed
import metrics

from copy import deepcopy

class Particle:
    def __init__(self, foreground_max_screen, background_max_screen, foreground_min_screen, background_min_screen, foreground_intersection, background_intersection, portion):
        self.foreground_structure = None
        self.background_structure = None
        self.dummy_structure = None

        self.connecting_comp = []
        self.dummy_connecting_comp = []

        self.f_seed = None
        self.b_seed = None

        self.foreground_intersection = foreground_intersection
        self.background_intersection = background_intersection
        self.dummy_intersection = None

        self.foreground_max_screen = foreground_max_screen
        self.background_max_screen = background_max_screen
        self.foreground_min_screen = foreground_min_screen
        self.background_min_screen = background_min_screen
        self.dummy_max_screen = None
        self.dummy_min_screen = None

        self.portion = portion
        self.generate_connecting_comp(1, foreground_intersection[0], foreground_intersection[1], foreground_intersection[2], background_intersection[2])
        self.generate_structures()


    def generate_structures(self):

        xy_target = []
        for i in self.connecting_comp:
            xy_target.append(i.xy_pos())
             

        f_seed = gen_seed.get_seed(self.foreground_intersection)
        self.f_seed = f_seed
        f_seed_next_possible = gen_seed.get_next_possible(f_seed[-1])
        f_struct = structure.Structure(f_seed, f_seed_next_possible, 1)
        self.foreground_structure = f_struct
    
        b_seed = gen_seed.get_seed_2(self.background_intersection,self.portion)
        self.b_seed = b_seed
        b_seed_next_possible = gen_seed.get_next_possible(b_seed[-1])
        b_struct = structure.Structure(b_seed, b_seed_next_possible, self.portion)
        self.background_structure = b_struct

    def generate_connecting_comp(self,num,x,y,z_front, z_back):
        for i in range(num):
            connecting_component_x = connecting_comp.offset()
            connecting_component_y = connecting_comp.offset()
            cc = connecting_comp.connecting_structure(x+connecting_component_x, y+connecting_component_y, z_front, z_back)
            # cc = connecting_comp.connecting_structure(self.foreground_intersection[0]+connecting_component_x, self.foreground_intersection[1]+connecting_component_y, self.foreground_intersection[2], self.background_intersection[2])
            self.connecting_comp.append(cc)

    def generate_dummy_connecting_comp(self,num,x,y,z_front, z_back):
        for i in range(num):
            cc = connecting_comp.connecting_structure(x, y, z_front, z_back)
            self.connecting_comp.append(cc)
            self.dummy_connecting_comp.append(cc)

    def generate_dummy_comp(self, dummy_max_screen, dummy_min_screen, dummy_intersection, dummy_portion):
        self.dummy_intersection = dummy_intersection
        self.dummy_max_screen = dummy_max_screen
        self.dummy_min_screen = dummy_min_screen

        d_seed = gen_seed.get_seed(dummy_intersection)
        d_seed_next_possible = gen_seed.get_next_possible(d_seed[-1])
        d_struct = structure.Structure(d_seed, d_seed_next_possible, dummy_portion)
        self.dummy_structure = d_struct

        for i in range(1):
            connecting_component_x = connecting_comp.offset()
            connecting_component_y = connecting_comp.offset()
            self.generate_dummy_connecting_comp(1, dummy_intersection[0]+connecting_component_x, dummy_intersection[1]+connecting_component_y, self.foreground_intersection[2], dummy_intersection[2])

    def generate_one(self):
        self.foreground_structure.generate(1)
        self.background_structure.generate(1)
        self.dummy_structure.generate(3)
    
        

    def finish(self):
        # self.generate_dummy_connecting_comp(1, self.foreground_structure.min_x, self.foreground_structure.min_y, self.foreground_intersection[2], self.dummy_intersection[2])
        # self.generate_dummy_connecting_comp(1, self.foreground_structure.max_x, self.foreground_structure.min_y, self.foreground_intersection[2], self.dummy_intersection[2])

        xy_targets = self.get_xy_target()
        self.foreground_structure.to_dest(xy_targets)
        self.background_structure.to_dest(xy_targets)

        dummy_xy_targets = self.get_dummy_xy_target()
        self.dummy_structure.to_dest(dummy_xy_targets)
    
    def get_xy_target(self):
        xy_targets = []
        for i in self.connecting_comp:
            xy_targets.append(i.xy_pos())
        return xy_targets
    
    def get_dummy_xy_target(self):
        xy_targets = []
        for i in self.dummy_connecting_comp:
            xy_targets.append(i.xy_pos())
        return xy_targets

    def is_off_screen(self):

        foreground_out_of_screen = metrics.out_of_screen(self.foreground_structure, self.foreground_max_screen, self.foreground_min_screen)
        background_out_of_screen = metrics.out_of_screen(self.background_structure, self.background_max_screen, self.background_min_screen)
        dummy_out_of_screen = metrics.out_of_screen(self.dummy_structure, self.dummy_max_screen, self.dummy_min_screen)

        if(foreground_out_of_screen or background_out_of_screen or dummy_out_of_screen):
            return -1000
                  
        return 0

    def parallel_score(self):
        (score, parallel_pts) = metrics.parallel_score(np.round(self.foreground_structure.history,1), np.round(self.background_structure.history,1))
        return score, parallel_pts
    
    def occulusion_score(self):
        score = 0
        eye = np.array([5.0,5.0,5.0])

        critical_pts = []

        for i in self.connecting_comp:
            cc_center = i.get_center()
            cc_fore = np.array([cc_center[0], cc_center[1], self.foreground_intersection[2]])
            cc_back = np.array([cc_center[0], cc_center[1], self.background_intersection[2]])
            critical_pts.append(cc_fore)
            critical_pts.append(cc_back)
            critical_pts.append(cc_center)
        
        for i in self.dummy_connecting_comp:
            cc_center = i.get_center()
            cc_fore = np.array([cc_center[0], cc_center[1], self.foreground_intersection[2]])
            cc_back = np.array([cc_center[0], cc_center[1], self.dummy_intersection[2]])
            critical_pts.append(cc_fore)
            critical_pts.append(cc_back)
            critical_pts.append(cc_center)

        critical_count = metrics.occlusion_score(self.foreground_structure,critical_pts, eye)
        critical_score = critical_count * -100

        seed_count = metrics.occlusion_score(self.foreground_structure,self.background_structure.seed, eye)
        seed_score = seed_count * -100

        cc_score = 0
        for i in self.connecting_comp:
            cc_pts = i.get_sample_points()
            cc_score += metrics.occlusion_score_wDist(self.foreground_structure,cc_pts, eye, 2, self.foreground_intersection[2], self.background_intersection[2])

        structure_score = metrics.occlusion_score_structures(self.foreground_structure, self.background_structure, eye)
        # print("critical_score: ", critical_score, " seed_score: ", seed_score, " cc_score: ", cc_score, " structure_score: ", structure_score)
        return critical_score + seed_score + cc_score + structure_score

    def too_close_score(self):
        if metrics.too_close(self.foreground_structure) or metrics.too_close(self.background_structure) or metrics.too_close(self.dummy_structure):
            return -100
        
        return 0
    
    def size_score(self):
        self.foreground_structure.get_MaxMin()
        self.background_structure.get_MaxMin()
        return metrics.size_score(self.foreground_structure, self.background_structure)
    
    def total_score(self):
        score = 2000000
        score += self.is_off_screen()
        score += self.too_close_score()
        score += self.occulusion_score()
        score += self.size_score()
        # (para_score, parallel_pts) = self.parallel_score()
        # score += para_score
        return score



def resample(particle_list, score_list):
    num_particles = len(particle_list)
    num_favorable = int(num_particles / 10)
    new_particle_list = []

    sorted_index = sorted(range(len(score_list)), key=lambda k: score_list[k])
    sorted_index.reverse()

    considered_total = 0

    for i in range(num_favorable):
        best_index = sorted_index[i]
        considered_total += score_list[best_index]

    for i in range(num_favorable):
        best_index = sorted_index[i]
        cur_score = score_list[best_index]
        num_copies = int(cur_score/considered_total * num_particles)

        for j in range(num_copies):
            cur_particle = deepcopy(particle_list[best_index])
            new_particle_list.append(cur_particle)
    
    for i in range(num_particles - len(new_particle_list)):
        best_index = sorted_index[0]
        cur_particle = deepcopy(particle_list[best_index])
        new_particle_list.append(cur_particle)

    return new_particle_list