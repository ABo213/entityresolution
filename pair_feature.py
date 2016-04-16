from distance import edit_dist
from distance import euclidean_dist
from distance import jaccard_dist
#from distance import dist_phone
from distance import my_jaccard_dist
from distance import dist_address1
from distance import dist_phone1
from distance import dist_phone2
from distance import fuzzy_address
#from distance import combined_name_phone_dist



dist_func_list =[
    (dist_phone1, 'phone'),
    (dist_phone2, 'phone'),
    (my_jaccard_dist, 'name'),
    #(edit_dist, 'name'),
    #(dist_phone, 'phone'),
    (fuzzy_address, 'street_address')
]

def generate_feature_list(a, b):
    features = []
    for func, field in dist_func_list:
        features.append(func(a[field], b[field]))
    if a["longitude"] and a["latitude"] and b["longitude"] and b["latitude"]:
        features.append(euclidean_dist(tuple((float(a["longitude"]),float(a["latitude"]))), tuple((b["longitude"],b["latitude"]))))
    else:
        #features.append(0.2)
        features.append(0.02)
    #features.append(combined_name_phone_dist(a['name'],b['name'],a['phone'],b['phone']))
    return features
    


 

