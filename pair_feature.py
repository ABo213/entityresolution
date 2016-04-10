from distance import edit_dist
from distance import euclidean_dist
from distance import jaccard_dist
from distance import dist_phone
from distance import my_jaccard_dist
from distance import dist_address




dist_func_list =[
    (my_jaccard_dist, 'name'),
    (edit_dist, 'name'),
    (dist_phone, 'phone'),
    (dist_address, 'street_address')
]

def generate_feature_list(a, b):
    features = []
    for func, field in dist_func_list:
        features.append(func(a[field], b[field]))
    return features
    


 

