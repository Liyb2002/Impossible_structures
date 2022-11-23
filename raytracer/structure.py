import numpy as np
import random

class Structure:
    def __init__(self, seed, seed_next_possible, portion, destination):
        self.history = None
        self.data = None
        self.rect = []
        self.next_possibles = None
        
        self.portion = portion
        self.seed = seed
        self.seed_next_possible = seed_next_possible
        
        self.cleanUp()
        self.destination = destination
        self.generate(3)
        self.to_dest()

        #print("initialized data: \n", self.data)
    

    def to_dest(self):
        next_vertex = self.next_possibles[rand_index(self.next_possibles)]
        x_dist = abs(self.destination[0] - next_vertex[0])
        x_start = min(self.destination[0], next_vertex[0])
        startPos = np.array([x_start, next_vertex[1], next_vertex[2]])
        scale = np.array([x_dist+0.07*self.portion, 0.07*self.portion, 0.07*self.portion])
        rect1 = rect(startPos, scale)
        
        y_dist = abs(self.destination[1] - next_vertex[1])
        y_start = min(self.destination[1], next_vertex[1])
        startPos2 = np.array([self.destination[0], y_start, next_vertex[2]])
        scale2 = np.array([0.07,y_dist+0.07*self.portion, 0.07*self.portion])
        rect2 = rect(startPos2, scale2)
        
        self.rect.append(rect1)
        self.rect.append(rect2)
        
        
    def cleanUp(self):
        self.history = self.seed
        self.data = np.array([[0.0,0.0,0.0]])
        self.data = np.append(self.data, self.seed, axis = 0)
        self.rect = []
        self.rect.append(block_to_rect(self.data, self.portion))
        self.data = np.array([[0.0,0.0,0.0]])
        self.next_possibles = self.seed_next_possible

  
    def cost_func(self, pos):
        return random.random()
  
    def add_vertex(self, next_vertex):
        x = next_vertex[0]
        y = next_vertex[1]
        z = next_vertex[2]

        self.data = np.vstack([self.data, np.array([x,y,z])])

    def remove_possible(self, next_index):
        self.next_possibles = np.delete(self.next_possibles, next_index, axis=0)
  
  #define direction:
  #x=-1 -> 0, x=1 -> 1, y=-1 -> 2, y=1 -> 3, z=-1 -> 4, z=1 -> 5,
    def get_next_possible(self, available_contact, direction):
        result = np.array([0,0,0,0])

        available_contact = np.append(available_contact, 0)
        if direction == 0 or direction == 1:
            result = np.vstack([result, available_contact + np.array([0.0,0.07,0.0,3])])
            result = np.vstack([result, available_contact + np.array([0.0,-0.07,0.0,2])])
            result = np.delete(result, 0, axis =0)
            return result

        if direction == 2 or direction == 3:
            result = np.vstack([result, available_contact + np.array([0.07,0.0,0.0,1])])
            result = np.vstack([result, available_contact + np.array([-0.07,0.0,0.0,1])])
            result = np.delete(result, 0, axis =0)
            return result

    
    def get_last_direction(self,direction):
        count =direction[1]*1 + direction[2]*2
        return count
  
    def get_vertex_forward(self, new_vertex_clean, direction):
        if direction == 0:
            return new_vertex_clean + np.array([-0.07,0.0,0.0])

        if direction == 1:
            return new_vertex_clean + np.array([0.07,0.0,0.0])

        if direction == 2:
            return new_vertex_clean + np.array([0.0,-0.07,0.0])

        if direction == 3:
            return new_vertex_clean + np.array([0.0,0.07,0.0])
    
    def generate(self, steps):
        for i in range(steps):
            #print("step ", i+1)
            self.process()
            self.history = np.append(self.history, self.data[1:], axis=0)
            self.rect.append(block_to_rect(self.data, self.portion))
            self.data = np.array([[0,0,0]])



    def process(self):
        #step 1: for all available contacts, assume they will make a turn  
        #print("next_possibles", self.next_possibles)

        #step2: create a 1d array that stores cost for each possible point
        costs = np.array([])
        for next_possible in self.next_possibles:
            costs = np.append(costs, self.cost_func(next_possible))

        #print("costs", costs)

        #step3 find the next_vertex with smallest cost
        next_index = np.argpartition(costs, -1)[-1:]
        next_vertex = self.next_possibles[next_index] 

        #print("next_vertex", next_vertex)

        #step4 add next_vertex to data
        new_direction = next_vertex[0][3]
        #print("new_direction", new_direction)
        new_vertex_clean = np.array([next_vertex[0][0], next_vertex[0][1], next_vertex[0][2]])
        #print("new_vertex_clean", new_vertex_clean)
        self.add_vertex(new_vertex_clean)
        
        span = 3 + int(random.random() * 6 % 6)
        for i in range(span):
            new_vertex_clean = self.get_vertex_forward(new_vertex_clean, new_direction)
            self.add_vertex(new_vertex_clean)

        #print("data: \n", self.data)

        #step5 update next_possible
        self.remove_possible(next_index)
        #print("next_possibles, removed old", self.next_possibles)
        #print("next_vertex", new_vertex_clean)
        #print("new_direction", new_direction)
        new_next_possibles = self.get_next_possible(new_vertex_clean, new_direction)
        self.next_possibles = np.append(self.next_possibles,new_next_possibles, axis=0)
        #print("next_possibles, add new", self.next_possibles)


class rect:
    def __init__(self, startPos, scale): 
        self.start_x = round(startPos[0],2)
        self.start_y = round(startPos[1],2)
        self.start_z = round(startPos[2],2)
        
        self.scale_x = round(scale[0],2)
        self.scale_y = round(scale[1],2)
        self.scale_z = round(scale[2],2)
    
    def info(self):
        print("start_x:",self.start_x,"start_y:",self.start_y,"start_z:",self.start_z)
        print("scale_x:",self.scale_x,"scale_y:",self.scale_y,"scale_z:",self.scale_z)
        print(" ")
    
def block_to_rect(buffer, portion):
    start = buffer[1]
    end = buffer[-1]
    x_start = min(start[0],end[0])
    y_start = min(start[1],end[1])    
    z_start = min(start[2],end[2])
    
    x_scale = max(abs(start[0] - end[0]), 0.07 * portion)
    y_scale = max(abs(start[1] - end[1]), 0.07 * portion)
    z_scale = max(abs(start[2] - end[2]), 0.07 * portion)
    
    if(x_scale > 0.07 * portion):
        x_scale += 0.07 * portion
        
    if(y_scale > 0.07 * portion):
        y_scale += 0.07 * portion
        
    if(z_scale > 0.07 * portion):
        z_scale += 0.07 * portion

    startPos = np.array([x_start,y_start,z_start])
    scale = np.array([x_scale,y_scale,z_scale])
    
    tempt = rect(startPos, scale)
    return tempt


def check_close(struct_a, struct_b):
    for i in struct_a.rect:
        for j in struct_b.rect:
            dist_x = abs(i.center_x() - j.center_x())
            dist_y = abs(i.center_y() - j.center_y())
            
            if dist_x < 0.2 or dist_y <0.2:
                return True
    return False

def rand_index(input_array):
    return int(random.random()* len(input_array) % len(input_array))