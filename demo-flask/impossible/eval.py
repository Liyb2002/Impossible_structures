import procedural_objects
import read_file
import sys
import random
import numpy as np
import cycle_connect
import produce
from tqdm import tqdm

def random_3d_position(max_abs_value=5):
    x = random.uniform(-max_abs_value, max_abs_value)
    y = random.uniform(-max_abs_value, max_abs_value)
    z = random.uniform(-max_abs_value, max_abs_value)

    return np.array([x, y, z])

def create_object(generic_object_list):
    obj_type = random.randint(0, len(generic_object_list)-5)
    obj_pos = random_3d_position()

    dummy_scope = np.array([[0.1,0.1], [0.1,0.1], [0.1,0.1]])
    dummy_offset = np.array([0,0,0])
    dummy_rotation = np.array([[0.0,0.0], [0.0,0.0], [0.0,0.0]])
    dummy_gen_hash = random.random()

    obj = procedural_objects.Procedural_object(obj_type, obj_pos, dummy_scope, dummy_gen_hash, dummy_rotation, dummy_offset)
    return obj


def random_test(generic_object_list):
    #Create two random procedural objects in 3D space
    obj1 = create_object(generic_object_list)
    obj2 = create_object(generic_object_list)

    delta = obj1.position - obj2.position
    abs_delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])
    abs_delta -= np.array([0, 0, obj2.length[2]])

    directions = cycle_connect.get_dirs(delta)
    orders = cycle_connect.random_order()

    production_list= [obj1]
    #Attempt to stablish connection

    success_connect = True
    for i in range(0,3):
        index = orders[i]
        if abs_delta[index] != 0:
            if i < 2:
                target_dir_index = orders[i+1]
                available_endings = cycle_connect.Available_Ending_With_Direction(generic_object_list, directions[target_dir_index])
            if i == 2:
                available_endings = cycle_connect.Available_Ending_With_Object(generic_object_list, obj2)

            connect_particle = produce.connect_execution(production_list[-1], generic_object_list,abs_delta,directions[index],available_endings, obj2)
            ok = 1

            while ok == 1:
                ok = connect_particle.execute_model_withDirection()
            
            if ok == 0:
                success_connect = False
                break 
            
            if ok == 2:
                break
    
    return success_connect


if __name__ == '__main__':
    #Load grammar
    if len(sys.argv) < 2:
        print("Usage: python eval.py <file_path> ")
        sys.exit(1)

    file_path = sys.argv[1]

    _, generic_object_list,_,_ = read_file.read_object_file(file_path)

    successes = 0
    for _ in tqdm(range(1000)):
        success = random_test(generic_object_list)
        if success:
            successes += 1

    print(f"Number of successes: {successes} out of 1000")
