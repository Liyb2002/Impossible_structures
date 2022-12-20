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
    def __init__(self, foreground_intersection, background_intersection, 
        portion, num_cc, block_size, Y_freedom, use_pixel):

        self.structures = []
        self.connecting_comp = []

        self.block_size = block_size

        self.foreground_intersection = foreground_intersection
        self.background_intersection = background_intersection

        self.portion = portion
        self.num_cc = num_cc
        self.Y_freedom = Y_freedom
        self.use_pixel = use_pixel


    def set_intersections(self,foreground_intersection, background_intersection, fore_portion, back_portion):
        intersect_type = random.randint(1,3)

        if self.Y_freedom:
            intersect_type = 1

        f_seed = gen_seed.get_seed(foreground_intersection, self.block_size, fore_portion, True, intersect_type)
        f_seed_next_possible = gen_seed.get_next_possible(f_seed[-1], self.block_size,True,intersect_type)
        f_struct = structure.Structure(f_seed, f_seed_next_possible, fore_portion, self.block_size)
        self.structures.append(f_struct)


        b_seed = gen_seed.get_seed(background_intersection, self.block_size, back_portion, False, intersect_type)
        b_seed_next_possible = gen_seed.get_next_possible(b_seed[-1], self.block_size,False,intersect_type)
        b_struct = structure.Structure(b_seed, b_seed_next_possible, back_portion, self.block_size)
        self.structures.append(b_struct)


    def get_connecting_comp(self, connections):
        for i in connections:
            layer1 = i[0]
            layer2 = i[1]

            struct1 = self.structures[layer1]
            front_z = struct1.seed[-1][2]
            struct2 = self.structures[layer2]
            back_z = struct2.seed[-1][2]

            x = struct1.seed[-1][0]
            y = struct1.seed[-1][1]

            self.generate_connecting_comp(self.num_cc, x, y, front_z, back_z, layer1, layer2)

    def generate_structures(self):

        xy_target = []
        for i in self.connecting_comp:
            xy_target.append(i.xy_pos())
             
        intersect_type = random.randint(1,4)

        if self.Y_freedom:
            intersect_type = random.randint(1,2)

        f_seed = gen_seed.get_seed(self.foreground_intersection, self.block_size, 1.0, True, intersect_type)
        f_seed_next_possible = gen_seed.get_next_possible(f_seed[-1], self.block_size,True,intersect_type)
        f_struct = structure.Structure(f_seed, f_seed_next_possible, 1, self.block_size)
        self.structures.append(f_struct)
        self.structures.append(f_struct)

        b_seed = gen_seed.get_seed(self.background_intersection, self.block_size, self.portion, False, intersect_type)
        b_seed_next_possible = gen_seed.get_next_possible(b_seed[-1], self.block_size,False,intersect_type)
        b_struct = structure.Structure(b_seed, b_seed_next_possible, self.portion, self.block_size)
        self.structures.append(b_struct)

    def generate_connecting_comp(self,num,x,y,z_front, z_back, layer1, layer2):
            connecting_component_x = connecting_comp.offset_x()
            connecting_component_y = connecting_comp.offset_y()

            cc = connecting_comp.connecting_structure(x+connecting_component_x, y+connecting_component_y, z_front, z_back, self.block_size)
            cc.set_layer(layer1, layer2)
            self.connecting_comp.append(cc)

    def generate_one(self, layer):
        self.structures[layer].generate(1)      

    def finish(self, step):
        for i in range(1, len(self.structures)):
            xy_targets = self.get_xy_target(i)
            if step == 0:
                self.structures[i].to_dest_1(xy_targets)
            elif step == 1:
                self.structures[i].to_dest_2(xy_targets)
    
    def get_xy_target(self, layer):
        xy_targets = []
        for i in self.connecting_comp:
            if i.layer1 == layer or i.layer2 == layer:
                xy_targets.append(i.xy_pos())
        return xy_targets
    
    def is_off_screen(self):

        foreground_out_of_screen = metrics.out_of_screen(self.structures[1], self.foreground_max_screen, self.foreground_min_screen)
        background_out_of_screen = metrics.out_of_screen(self.structures[2], self.background_max_screen, self.background_min_screen)

        if(foreground_out_of_screen or background_out_of_screen):
            return -1000
                  
        return 0

    def parallel_score(self):
        (score, parallel_pts) = metrics.parallel_score(np.round(self.structures[1].history,1), np.round(self.structures[2].history,1))
        return score, parallel_pts
    
    def occulusion_score(self):
        eye = np.array([5.0,5.0,5.0])

        raster_score = 0
        if self.use_pixel:
            for i in range(2, len(self.structures)):
                raster_score += metrics.occlusion_raster(self.structures[i-1], self.structures[i])

        critical_pts = []

        for i in self.connecting_comp:
            cc_center = i.get_center()
            cc_fore = np.array([cc_center[0], cc_center[1], self.foreground_intersection[2]])
            cc_back = np.array([cc_center[0], cc_center[1], self.background_intersection[2]])
            critical_pts.append(cc_fore)
            critical_pts.append(cc_back)
            critical_pts.append(cc_center)
        
        critical_count = 0
        for i in self.structures:
            critical_count += metrics.occlusion_score(i,critical_pts, eye)
        critical_score = critical_count * -30

        seed_count = 0
        for i in self.structures:
            for j in self.structures:
                seed_count += metrics.occlusion_score(j,i.seed, eye)
        seed_score = seed_count * -30

        cc_score = 0
        for i in self.connecting_comp:
            cc_pts = i.get_sample_points()
            cc_score += metrics.occlusion_score_wDist(self.structures[1],cc_pts, eye, 2, self.foreground_intersection[2], self.background_intersection[2])
        
        structure_score = 0
        for i in self.structures:
            for j in self.structures:
                structure_score += metrics.occlusion_score_structures(i,j, eye)
        return critical_score + seed_score + cc_score + structure_score + raster_score + 100

    def too_close_score(self):
        score = 5 * len(self.structures)
        for i in self.structures:
            if metrics.too_close(i):
                score -= 5
        return score
    
    def size_score(self):
        self.structures[1].get_MaxMin()
        self.structures[2].get_MaxMin()
        return metrics.size_score(self.structures[1], self.structures[2])
    
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

            if dist2 != 0:
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
        for i in self.structures[1].rect:
            point = i.center()
            point = np.matmul(m_view, point.T)
            point = np.matmul(m_proj, point)

            if interpolation.PointInTriangle(point, foreground_loc, background_loc, intersection_loc):
                count += 1

        for i in self.structures[2].rect:
            point = i.center()
            point = np.matmul(m_view, point.T)
            point = np.matmul(m_proj, point)

            if interpolation.PointInTriangle(point, foreground_loc, background_loc, intersection_loc):
                count += 1

        return count

    def total_score(self):
        score = 0
        # score += self.is_off_screen()
        score += self.too_close_score()
        score += self.occulusion_score()
        score += self.size_score()
        score += self.triangle_score()
        # (para_score, parallel_pts) = self.parallel_score()
        # score += para_score
        # print("self.too_close_score()", self.too_close_score(), "self.occulusion_score()", self.occulusion_score(), "self.size_score()", self.size_score(), "self.triangle_score()", self.triangle_score())
        # print("score: ", score)
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