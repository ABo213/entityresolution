from scipy.spatial import distance

def euclidean_dist(pos_1, pos_2):
    return distance.euclidean(pos_1, pos_2)