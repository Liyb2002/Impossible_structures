import procedural_objects

def reduce(list_all_obj):
    list_unique_obj = []

    for obj in list_all_obj:
        unique = True
        for unique_obj in list_unique_obj:
            if unique_obj.position[0] == obj.position[0] and unique_obj.position[1] == obj.position[1]  and unique_obj.position[2] == obj.position[2] :
                unique = False
                break
        
        if unique == True:
            list_unique_obj.append(obj)
    
    return list_unique_obj
