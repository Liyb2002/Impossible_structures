import numpy as np

import intersection
import structure
import connecting_comp
import gen_seed
import metrics
import perspective
import interpolation

import random
from copy import deepcopy
import math

class Particle:
    def __init__(self, foreground_max_screen, background_max_screen, foreground_min_screen, background_min_screen, foreground_intersection, background_intersection, 
        portion, num_cc, block_size):
        self.foreground_structure = None
        self.background_structure = None
        self.dummy_structure = None

        self.connecting_comp = []
        self.dummy_connecting_comp = []

        self.f_seed = None
        self.b_seed = None

        self.block_size = block_size

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
        self.num_cc = num_cc

        self.extra_foreground = None
        self.extra_background = None

    def set_intersections(self,foreground_intersection, background_intersection, fore_portion, back_portion):
        intersect_type = random.randint(1,4)
        intersect_type = 3

        f_seed = gen_seed.get_seed(foreground_intersection, self.block_size, fore_portion, True, intersect_type)
        f_seed_next_possible = gen_seed.get_next_possible(f_seed[-1], self.block_size,True,intersect_type)
        f_struct = structure.Structure(f_seed, f_seed_next_possible, 1, self.block_size)
        self.extra_foreground = f_struct
        connecting_component_x = connecting_comp.offset()
        connecting_component_y = connecting_comp.offset()
        f_cc = connecting_comp.connecting_structure(connecting_component_x, connecting_component_y, self.foreground_intersection[2], foreground_intersection[2], self.block_size)
        self.connecting_comp.append(f_cc)
        dest = []
        dest.append(np.array([connecting_component_x, connecting_component_y, foreground_intersection[2]]))
        f_struct.to_dest(dest)


        b_seed = gen_seed.get_seed(background_intersection, self.block_size, back_portion, False, intersect_type)
        b_seed_next_possible = gen_seed.get_next_possible(b_seed[-1], self.block_size,False,intersect_type)
        b_struct = structure.Structure(b_seed, b_seed_next_possible, back_portion, self.block_size)
        self.extra_background = b_struct
        connecting_component_x = connecting_comp.offset()
        connecting_component_y = connecting_comp.offset()
        b_cc = connecting_comp.connecting_structure(connecting_component_x, connecting_component_y, self.foreground_intersection[2], background_intersection[2], self.block_size)
        self.connecting_comp.append(b_cc)
        dest = []
        dest.append(np.array([connecting_component_x, connecting_component_y, foreground_intersection[2]]))
        b_struct.to_dest(dest)


    def get_connecting_comp(self):
        self.generate_connecting_comp(self.num_cc, self.foreground_intersection[0], self.foreground_intersection[1], self.foreground_intersection[2], self.background_intersection[2])

    def generate_structures(self):

        xy_target = []
        for i in self.connecting_comp:
            xy_target.append(i.xy_pos())
             
        intersect_type = random.randint(1,2)
        intersect_type = 1
        f_seed = gen_seed.get_seed(self.foreground_intersection, self.block_size, 1.0, True, intersect_type)
        self.f_seed = f_seed
        f_seed_next_possible = gen_seed.get_next_possible(f_seed[-1], self.block_size,True,intersect_type)
        f_struct = structure.Structure(f_seed, f_seed_next_possible, 1, self.block_size)
        self.foreground_structure = f_struct
    
        b_seed = gen_seed.get_seed(self.background_intersection, self.block_size, self.portion, False, intersect_type)
        self.b_seed = b_seed
        b_seed_next_possible = gen_seed.get_next_possible(b_seed[-1], self.block_size,False,intersect_type)
        b_struct = structure.Structure(b_seed, b_seed_next_possible, self.portion, self.block_size)
        self.background_structure = b_struct

    def generate_connecting_comp(self,num,x,y,z_front, z_back):
        offsets = []
        for i in range(num):
            valid_offset = False

            connecting_component_x = connecting_comp.offset()
            connecting_component_y = connecting_comp.offset()
            tempt_pt = np.array([connecting_component_x, connecting_component_y])

            while valid_offset == False:
                valid_offset = connecting_comp.valid_offset(offsets, tempt_pt)
                connecting_component_x = connecting_comp.offset()
                connecting_component_y = connecting_comp.offset()
                tempt_pt = np.array([connecting_component_x, connecting_component_y])

            cc = connecting_comp.connecting_structure(x+connecting_component_x, y+connecting_component_y, z_front, z_back, self.block_size)
            self.connecting_comp.append(cc)

    def generate_dummy_connecting_comp(self,num,x,y,z_front, z_back):
        for i in range(num):
            cc = connecting_comp.connecting_structure(x, y, z_front, z_back, self.block_size)
            self.connecting_comp.append(cc)
            self.dummy_connecting_comp.append(cc)

    def generate_dummy_comp(self, dummy_max_screen, dummy_min_screen, dummy_intersection, dummy_portion, dummy_cc):
        self.dummy_intersection = dummy_intersection
        self.dummy_max_screen = dummy_max_screen
        self.dummy_min_screen = dummy_min_screen

        d_seed = gen_seed.get_seed(dummy_intersection, self.block_size)
        d_seed_next_possible = gen_seed.get_next_possible(d_seed[-1], self.block_size)
        d_struct = structure.Structure(d_seed, d_seed_next_possible, dummy_portion, self.block_size)
        self.dummy_structure = d_struct

        for i in range(dummy_cc):
            connecting_component_x = connecting_comp.offset()
            connecting_component_y = connecting_comp.offset()
            self.generate_dummy_connecting_comp(1, dummy_intersection[0]+connecting_component_x, dummy_intersection[1]+connecting_component_y, self.foreground_intersection[2], dummy_intersection[2])

    def generate_one(self):
        self.foreground_structure.generate(1)
        self.background_structure.generate(1)
        self.dummy_structure.generate(1)
    

    def finish(self):

        xy_targets = self.get_xy_target()
        self.foreground_structure.to_dest(xy_targets)
        self.background_structure.to_dest(xy_targets)

        dummy_xy_targets = self.get_dummy_xy_target()
        if self.dummy_structure != None:
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

        # raster_score = metrics.occlusion_raster(self.foreground_structure, self.background_structure)

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
            return -20
        return 0
    
    def size_score(self):
        self.foreground_structure.get_MaxMin()
        self.background_structure.get_MaxMin()
        return metrics.size_score(self.foreground_structure, self.background_structure)
    
    def triangle_score(self):
        intersection_loc = np.array([self.foreground_intersection[0],self.foreground_intersection[1],self.foreground_intersection[2], 1])
        m_view = perspective.get_m_view()
        m_proj = perspective.get_m_proj()
        intersection_loc = np.matmul(m_view, intersection_loc.T)
        intersection_loc = np.matmul(m_proj, intersection_loc)

        triangle_score = 0
        for cc in self.connecting_comp:
            cc_triangle_score = 0
            x = cc.x
            y = cc.y
            foreground_z = cc.foreground_z
            background_z = cc.background_z

            foreground_loc = np.array([x,y,foreground_z,1])
            foreground_loc = np.matmul(m_view, foreground_loc.T)
            foreground_loc = np.matmul(m_proj, foreground_loc)

            background_loc = np.array([x,y,background_z,1])
            background_loc = np.matmul(m_view, background_loc.T)
            background_loc = np.matmul(m_proj, background_loc)

            #pixles inside triangle
            count = self.tirangle_occulusion(foreground_loc, background_loc, intersection_loc, m_view, m_proj)
            pixle_score = 10 - count
            # print("pixle_score: ", pixle_score)
            cc_triangle_score += pixle_score

            #ratio
            ratio_score = 10
            mid_point = interpolation.mid_cc(foreground_loc, background_loc)
            dist1 = interpolation.dist_pt(mid_point, intersection_loc)
            dist2 = interpolation.dist_pt(foreground_loc, background_loc)

            r = dist1 / dist2
            if r < 0.6 or r > 0.9:
                ratio_score -= metrics.triangle_property_score(r)
            # print("ratio_score: ", ratio_score)
            cc_triangle_score += ratio_score

            #cc on screen size
            screen_cc_score = dist2 ** 2
            # print("screen_cc_score: ", screen_cc_score)
            cc_triangle_score += screen_cc_score

        triangle_score += cc_triangle_score
        # print("triangle_score: ", triangle_score)
        return triangle_score 

    def tirangle_occulusion(self, foreground_loc, background_loc, intersection_loc, m_view, m_proj):
        count = 0
        for i in self.foreground_structure.rect:
            point = i.center()
            point = np.matmul(m_view, point.T)
            point = np.matmul(m_proj, point)

            if interpolation.PointInTriangle(point, foreground_loc, background_loc, intersection_loc):
                count += 1

        for i in self.background_structure.rect:
            point = i.center()
            point = np.matmul(m_view, point.T)
            point = np.matmul(m_proj, point)

            if interpolation.PointInTriangle(point, foreground_loc, background_loc, intersection_loc):
                count += 1

        return count

    def total_score(self):
        score = 2000000
        score += self.is_off_screen()
        score += self.too_close_score()
        score += self.occulusion_score()
        score += self.size_score()
        score += self.triangle_score()
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