import numpy as np
import random

class Procedural_object:
    def __init__(self, type, position, scope, gen_hash, next_rotation, next_offset):
        self.type = type
        self.position = position
        self.scope = scope
        self.set_scope()
        self.hash = gen_hash
        self.connected = []
        self.rotation = np.array([random.choice(next_rotation[0]), random.choice(next_rotation[1]), random.choice(next_rotation[2])])
        self.offset = next_offset

        self.group = 1

    def set_type(self, type):
        self.type = type
    
    def set_group(self, group):
        self.group = group
        
    def set_scope(self):
        scope_x = self.scope[0]
        scope_y = self.scope[1]
        scope_z = self.scope[2]

        len_x = round(random.uniform(scope_x[0], scope_x[1]),4)
        len_y = round(random.uniform(scope_y[0], scope_y[1]),4)
        len_z = round(random.uniform(scope_z[0], scope_z[1]),4)
        self.length = np.array([len_x, len_y, len_z])

    def set_position(self, prev_obj, rule):
        prev_pos = prev_obj.position
        prev_x = prev_obj.length[0]
        prev_y = prev_obj.length[1]
        prev_z = prev_obj.length[2]

        offset =  np.array([self.offset[0],self.offset[1],self.offset[2]])
        self.position = prev_pos + offset

        if(rule == '-x'):
            prev_obj_closest_point = prev_obj.position - np.array([prev_obj.length[0], 0, 0])
            prev_obj_rotated_point = rotate_line(self.position, prev_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

            new_obj_closest_point = np.array([self.length[0], 0, 0])
            new_obj_rotated_point = rotate_line(np.array([0,0,0]), new_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

            # self.position += -np.array([prev_obj.length[0], 0, 0]) - np.array([self.length[0],0 , 0]) + prev_obj_delta_rotate + new_obj_delta_rotate
            self.position = self.position -np.array([prev_obj.length[0], 0, 0]) - np.array([self.length[0],0 , 0])

        if(rule == '+x'):
            prev_obj_closest_point = prev_obj.position + np.array([prev_obj.length[0], 0, 0])
            prev_obj_rotated_point = rotate_line(self.position, prev_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

            new_obj_closest_point = np.array([-self.length[0], 0, 0])
            new_obj_rotated_point = rotate_line(np.array([0,0,0]), new_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

            # self.position += np.array([prev_obj.length[0], 0, 0]) + np.array([self.length[0],0 , 0]) + prev_obj_delta_rotate + new_obj_delta_rotate
            self.position += np.array([prev_obj.length[0], 0, 0]) + np.array([self.length[0],0 , 0])

        if(rule == '-y'):
            prev_obj_closest_point = prev_obj.position - np.array([0, prev_obj.length[1], 0])
            prev_obj_rotated_point = rotate_line(self.position, prev_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

            new_obj_closest_point = np.array([0, self.length[1], 0])
            new_obj_rotated_point = rotate_line(np.array([0,0,0]), new_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

            # self.position += -np.array([0, prev_obj.length[1], 0]) - np.array([0,self.length[1] , 0]) + prev_obj_delta_rotate + new_obj_delta_rotate
            self.position = self.position - np.array([0, prev_obj.length[1], 0]) - np.array([0,self.length[1] , 0])

        if(rule == '+y'):
            prev_obj_closest_point = prev_obj.position + np.array([0, prev_obj.length[1], 0])
            prev_obj_rotated_point = rotate_line(self.position, prev_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

            new_obj_closest_point = np.array([0, -self.length[1], 0])
            new_obj_rotated_point = rotate_line(np.array([0,0,0]), new_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

            # self.position += np.array([0, prev_obj.length[1], 0]) + np.array([0,self.length[1] , 0]) + prev_obj_delta_rotate + new_obj_delta_rotate
            self.position += np.array([0, prev_obj.length[1], 0]) + np.array([0,self.length[1] , 0])

        if(rule == '-z'):
            prev_obj_closest_point = prev_obj.position - np.array([0, 0, prev_obj.length[2]])
            prev_obj_rotated_point = rotate_line(self.position, prev_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

            new_obj_closest_point = np.array([0,0, self.length[2]])
            new_obj_rotated_point = rotate_line(np.array([0,0,0]), new_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

            # self.position += -np.array([0, 0, prev_obj.length[2]]) - np.array([0,0 ,self.length[2]]) + prev_obj_delta_rotate + new_obj_delta_rotate
            self.position =self.position -np.array([0, 0, prev_obj.length[2]]) - np.array([0,0 ,self.length[2]])

        if(rule == '+z'):
            prev_obj_closest_point = prev_obj.position + np.array([0, 0, prev_obj.length[2]])
            prev_obj_rotated_point = rotate_line(self.position, prev_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            prev_obj_delta_rotate = prev_obj_rotated_point - prev_obj_closest_point

            new_obj_closest_point = np.array([0,0, -self.length[2]])
            new_obj_rotated_point = rotate_line(np.array([0,0,0]), new_obj_closest_point, self.rotation[0],self.rotation[1],self.rotation[2])
            new_obj_delta_rotate = new_obj_rotated_point - new_obj_closest_point

            # self.position += np.array([0, 0, prev_obj.length[2]]) + np.array([0,0 ,self.length[2]]) + prev_obj_delta_rotate + new_obj_delta_rotate
            self.position += np.array([0, 0, prev_obj.length[2]]) + np.array([0,0 ,self.length[2]])

        if(rule == '-x2'):
            self.position = prev_pos - np.array([prev_x, -prev_y, 0]) - np.array([self.length[0],0 ,0])
            self.arriving_rule = '-x'
            
        self.arriving_rule = rule
        self.adjust_rotation(prev_obj)
        
    def adjust_rotation(self, prev_obj):
        prev_rotation = prev_obj.rotation

        if self.rotation[0] == 0.001:
            self.rotation = prev_rotation
            return

        for i in range(0,3):
            if prev_rotation[i] * self.rotation[i] > 0:
                self.rotation[i] = - self.rotation[i]

    def arbitrary_set_position(self, position):
        self.position = position

    def collision_check(self, objB):
        A_x = [self.position[0] - self.length[0], self.position[0] + self.length[0]]
        B_x = [objB.position[0] - objB.length[0], objB.position[0] + objB.length[0]]
        overlap_x = getOverlap(A_x, B_x)

        A_y = [self.position[1] - self.length[1], self.position[1] + self.length[1]]
        B_y = [objB.position[1] - objB.length[1], objB.position[1] + objB.length[1]]
        overlap_y = getOverlap(A_y, B_y)

        A_z = [self.position[2] - self.length[2], self.position[2] + self.length[2]]
        B_z = [objB.position[2] - objB.length[2], objB.position[2] + objB.length[2]]
        overlap_z = getOverlap(A_z, B_z)

        if overlap_x>0.02 and overlap_y>0.02 and overlap_z>0.02:
            # print("cur obj", self.position, self.length)
            # print("objB", objB.position, objB.length)
            return True

        return False
    
    def add_connected(self, direction):
        for dir in self.connected:
            if dir == direction:
                return 
        self.connected.append(direction)

    def arbitrary_set_length(self, length):
        len_x = length[0]
        len_y = length[1]
        len_z = length[2]
        self.length = np.array([len_x, len_y, len_z])


def getOverlap3D(objectA_position, objectA_size, objectB_position, objectB_size):
    A_x = [objectA_position[0] - objectA_size[0], objectA_position[0] + objectA_size[0]]
    B_x = [objectB_position[0] - objectB_size[0], objectB_position[0] + objectB_size[0]]
    overlap_x = getOverlap(A_x, B_x)

    A_y = [objectA_position[1] - objectA_size[1], objectA_position[1] + objectA_size[1]]
    B_y = [objectB_position[1] - objectB_size[1], objectB_position[1] + objectB_size[1]]
    overlap_y = getOverlap(A_y, B_y)

    A_z = [objectA_position[2] - objectA_size[2], objectA_position[2] + objectA_size[2]]
    B_z = [objectB_position[2] - objectB_size[2], objectB_position[2] + objectB_size[2]]
    overlap_z = getOverlap(A_z, B_z)

    return overlap_x * overlap_y * overlap_z

def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

def rotate_line(line_center, line_endpoints, alpha_x_rad, alpha_y_rad, alpha_z_rad):
    # Translation to origin
    line_endpoints = line_endpoints - line_center

    # Rotation matrices
    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(alpha_x_rad), -np.sin(alpha_x_rad)],
                           [0, np.sin(alpha_x_rad), np.cos(alpha_x_rad)]])

    rotation_y = np.array([[np.cos(alpha_y_rad), 0, np.sin(alpha_y_rad)],
                           [0, 1, 0],
                           [-np.sin(alpha_y_rad), 0, np.cos(alpha_y_rad)]])

    rotation_z = np.array([[np.cos(alpha_z_rad), -np.sin(alpha_z_rad), 0],
                           [np.sin(alpha_z_rad), np.cos(alpha_z_rad), 0],
                           [0, 0, 1]])

    # Apply rotations to endpoints only
    line_endpoints = np.dot(rotation_x, line_endpoints.T).T
    line_endpoints = np.dot(rotation_y, line_endpoints.T).T
    line_endpoints = np.dot(rotation_z, line_endpoints.T).T

    # Translation back to original position
    line_endpoints = line_endpoints + line_center

    return line_endpoints
