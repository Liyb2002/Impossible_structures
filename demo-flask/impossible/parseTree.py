
def parseProb(generic_object_list, start_obj):
    parsedProb = {}
    current_level_nodes = []
    next_level_nodes = []

    for generic_obj in generic_object_list:
        parsedProb[generic_obj.id] = 0
    
    parsedProb[start_obj.id] = 1

    rootNode = treeNode(start_obj.id, 1.0)
    current_level_nodes.append(rootNode)

    #parse the tree
    steps = 10
    step = 0
    while step < steps:
        step += 1
        for node in current_level_nodes:
            cur_generic_id = node.generic_id
            cur_obj = generic_object_list[cur_generic_id]
            cur_prob = node.prob

            for prob_tuple in cur_obj.probabilities:
                newNode = treeNode(prob_tuple[0], cur_prob * prob_tuple[1])
                parsedProb[prob_tuple[0]] += cur_prob * prob_tuple[1]
                next_level_nodes.append(newNode)

        current_level_nodes = next_level_nodes
        next_level_nodes = []
    
    #normalize
    total_prob = 0
    for key in parsedProb:
        total_prob += parsedProb[key]
    
    for key in parsedProb:
        parsedProb[key] = parsedProb[key] / total_prob
        # print("generic id", key)
        # print("prob", parsedProb[key])

    return parsedProb

class treeNode:
    def __init__(self, generic_id, prob):
        self.generic_id = generic_id
        self.prob = prob
