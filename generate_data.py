import random

def generate_no_match(entities_a, entities_b, match_entity, size):
    no_matches = []
    id_a_list = entities_a.keys()
    id_b_list = entities_b.keys()
    random.shuffle(id_a_list)
    random.shuffle(id_b_list)
    index1 = 0
    index2 = 0
    for i in range(size):
        id1 = id_a_list[index1]
        id2 = id_a_list[index2]
        while tuple([id1, id2]) in match_entity:
            index1 += 1
            id1 = id_a_list[index1]
        no_matches.append(tuple([id1, id2]))
        index1 += 1
        index2 += 1
    return no_matches
            
        
        
        
        
        
        
    