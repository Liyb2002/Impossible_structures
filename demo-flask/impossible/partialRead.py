import json
import procedural_objects

def read_partial(file_path):
    procedural_object_list = []

    with open( file_path, 'r') as object_file:
        objects_data = json.load(object_file)

        generic_object_list.append(generic_objects.Generic_object(objects_data[1]))
        for object_data in objects_data:
            obj_hash = object_data['type'] + random.uniform(0, 1)
            obj_position = np.array([object_data['start_x']+object_data['scale_x'], object_data['start_y']+object_data['scale_y'], object_data['start_z']+object_data['scale_z']])
            obj_rotation = np.array([object_data['rotation_x'], object_data['rotation_y'], object_data['rotation_z']])
            obj_size = np.array([object_data['scale_x'], object_data['scale_y'], object_data['scale_z']])
            new_procedural_obj = procedural_objects.Procedural_object(object_data['type'], obj_position, np.array([0,0,0]), obj_hash, obj_rotation, np.array([0,0,0]))
            
            new_procedural_obj.arbitrary_set_length(obj_size)
            procedural_object_list.append(new_procedural_obj)
            

    return procedural_object_list