import numpy as np

import intersection
import structure
import connecting_comp
import gen_seed
import metrics

class Particle:
    def __init__(self):
        self.foreground_structure = None
        self.background_structure = None
        self.connecting_comp = None
        self.f_seed = None
        self.b_seed = None

        self.foreground_index = 8
        self.background_index = 12
        self.intersections = intersection.Scene()
        self.foreground_intersection = self.intersections.get_possible_intersects(self.foreground_index)
        self.background_intersection = self.intersections.get_possible_intersects(self.background_index)

        self.portion = self.background_index/self.foreground_index

        self.generate_connecting_comp()
        self.generate_structures()
        

    def generate_structures(self):

        f_seed = gen_seed.get_seed(self.foreground_intersection)
        self.f_seed = f_seed
        f_seed_next_possible = gen_seed.get_next_possible(f_seed[-1])
        f_struct = structure.Structure(f_seed, f_seed_next_possible, 1, self.connecting_comp.xy_pos())
        self.foreground_structure = f_struct
    
        b_seed = gen_seed.get_seed_2(self.background_intersection,self.portion)
        self.b_seed = b_seed
        b_seed_next_possible = gen_seed.get_next_possible(b_seed[-1])
        b_struct = structure.Structure(b_seed, b_seed_next_possible, self.portion,self.connecting_comp.xy_pos())
        self.background_structure = b_struct

    def generate_connecting_comp(self):
        connecting_component_x = connecting_comp.offset()
        connecting_component_y = connecting_comp.offset()
        cc = connecting_comp.connecting_structure(self.foreground_intersection[0]+connecting_component_x, self.foreground_intersection[1]+connecting_component_y, self.foreground_intersection[2], self.background_intersection[2])
        
        self.connecting_comp = cc
    
    def is_off_screen(self):

        #check off screen
        foreground_max_screen = self.intersections.get_max_screen(self.foreground_index)
        background_max_screen = self.intersections.get_max_screen(self.background_index)
        foreground_min_screen = self.intersections.get_min_screen(self.foreground_index)
        background_min_screen = self.intersections.get_min_screen(self.background_index)

        foreground_out_of_screen = metrics.out_of_screen(self.foreground_structure, foreground_max_screen, foreground_min_screen)
        background_out_of_screen = metrics.out_of_screen(self.background_structure, background_max_screen, background_min_screen)

        if(foreground_out_of_screen or background_out_of_screen):
            return -100
                  
        return 0

    def parallel_score(self):
        (score, parallel_pts) = metrics.parallel_score(np.round(self.foreground_structure.history,1), np.round(self.background_structure.history,1))
        return score, parallel_pts
    
    def occulusion_score(self):
        score = 0
        eye = np.array([5.0,5.0,5.0])
    
        cc_center = self.connecting_comp.get_center()
        cc_fore = np.array([cc_center[0], cc_center[1], self.foreground_intersection[2]])
        cc_back = np.array([cc_center[0], cc_center[1], self.background_intersection[2]])

        checkpts = []
        checkpts.append(cc_center)
        checkpts.append(cc_fore)
        checkpts.append(cc_back)
        checkpts.append(self.background_intersection)

        count = metrics.occlusion_score(self.foreground_structure,checkpts, eye)

        print("occulusion points", count)

        return count * -20

    def too_close_score(self):
        if metrics.too_close(self.foreground_structure) or metrics.too_close(self.background_structure):
            return -100
        
        return 0
    
    def total_score(self):
        score = 0
        score += self.is_off_screen()
        score += self.too_close_score()
        score += self.occulusion_score()
        (para_score, parallel_pts) = self.parallel_score()
        score += para_score
        return score