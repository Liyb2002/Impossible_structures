import intersection
import structure
import connecting_comp
import gen_seed

class Particle:
    def __init__(self):
        self.foreground_structure = None
        self.background_structure = None
        self.connecting_comp = None

        self.foreground_index = 8
        self.background_index = 12
        intersections = intersection.Scene()
        self.foreground_intersection = intersections.get_possible_intersects(self.foreground_index)
        self.background_intersection = intersections.get_possible_intersects(self.background_index)

        self.portion = self.background_index/self.foreground_index

        self.generate_connecting_comp()
        self.generate_structures()

    def generate_structures(self):

        f_seed = gen_seed.get_seed(self.foreground_intersection)
        f_seed_next_possible = gen_seed.get_next_possible(f_seed[-1])
        f_struct = structure.Structure(f_seed, f_seed_next_possible, 1, self.connecting_comp.xy_pos())
        self.foreground_structure = f_struct
    
        b_seed = gen_seed.get_seed_2(self.background_intersection,self.portion)
        b_seed_next_possible = gen_seed.get_next_possible(b_seed[-1])
        b_struct = structure.Structure(b_seed, b_seed_next_possible, self.portion,self.connecting_comp.xy_pos())
        self.background_structure = b_struct

    def generate_connecting_comp(self):
        connecting_component_x = connecting_comp.offset()
        connecting_component_y = connecting_comp.offset()
        cc = connecting_comp.connecting_structure(self.foreground_intersection[0]+connecting_component_x, self.foreground_intersection[1]+connecting_component_y, self.foreground_intersection[2], self.background_intersection[2])
        
        self.connecting_comp = cc
    
