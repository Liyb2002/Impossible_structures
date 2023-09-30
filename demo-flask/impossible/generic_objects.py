import random
import numpy as np

class Generic_object:
    def __init__(self, info):
        self.id = info['object_id']
        self.set_scope(info)
        self.connect_id = []
        self.canTerminate = info['canTerminate']
        self.rules = info['connect_rule']
        self.probabilities = []
        self.cycle_connect = info['cycle_connect']

        self.rotation = info['rotation']
        self.offsets = info['offsets']

        self.set_connect_ids(info['connect_id'])

    def set_connect_ids(self, id_tuples):
        for id_tuple in id_tuples:
            self.connect_id.append(id_tuple[0])
            self.probabilities.append(id_tuple)

    def get_offset(self, id):
        return self.offsets[str(id)]

    def get_nextType(self, unavailable_dirs):
        if self.connect_id == []:
            # print("terminate")
            return

        count = 0
        while count <3:
            rand = random.uniform(0, 1)
            sum_prob = 0
            count += 1

            for id_tuple in self.probabilities:
                sum_prob += id_tuple[1]
                if sum_prob >= rand:
                    choice = id_tuple[0]

            choice = random.choice(self.connect_id)
            direction = self.execute_rule(choice)
            available_next = True

            for unavailable_dir in unavailable_dirs:
                if direction == unavailable_dir:
                    available_next = False

            if available_next: 
                return choice
            
        return None
    
    def set_scope(self, info):
        multipler = 1.0
        scope_x = info['scope_x']
        scope_y = info['scope_y']
        scope_z = info['scope_z']

        scope_x = [scope_x[0] * multipler, scope_x[1] * multipler]
        scope_y = [scope_y[0] * multipler, scope_y[1] * multipler]
        scope_z = [scope_z[0] * multipler, scope_z[1] * multipler]

        self.scope = np.array([scope_x,scope_y,scope_z])
    
    def adjust_scope(self, multipler):
        scope_x = self.scope[0]
        scope_y = self.scope[1]
        scope_z = self.scope[2]

        scope_x = [scope_x[0] * multipler, scope_x[1] * multipler]
        scope_y = [scope_y[0] * multipler, scope_y[1] * multipler]
        scope_z = [scope_z[0] * multipler, scope_z[1] * multipler]

        self.scope = np.array([scope_x,scope_y,scope_z])

    def execute_rule(self, next_id):
        rule = self.rules[str(next_id)]
        choice = random.choice(rule)
        return choice

    def get_nextType_with_direction(self, direction):
        possible_next = []
        for next_id in self.rules:
            for i in range(len(self.rules[next_id])):
                if direction == self.rules[next_id][i]:
                    possible_next.append(next_id)
        
        if len(possible_next) != 0:
            choice = possible_next[0]
            rule = direction
        else:
            return (False, [], [])
        
        return (True,choice, rule)
        
    def able_next_direction(self, direction):
        for next_id in self.rules:
            for i in range(len(self.rules[next_id])):
                if direction == self.rules[next_id][i]:
                    return True

        return False    

    def test(self):
        print("hello")
    
    def generate_hash(self):
        gen_hash = self.id + random.uniform(0, 1)
        return gen_hash
