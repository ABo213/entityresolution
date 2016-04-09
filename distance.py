from scipy.spatial import distance
import re
def edit_dist(word1, word2):
    l1, l2 = len(word1)+1, len(word2)+1
    pre = [0 for _ in xrange(l2)]
    for j in xrange(l2):
        pre[j] = j
    for i in xrange(1, l1):
        cur = [i]*l2
        for j in xrange(1, l2):
            cur[j] = min(cur[j-1]+1, pre[j]+1, pre[j-1]+(word1[i-1]!=word2[j-1]))
        pre = cur[:]
    return pre[-1]
    
def euclidean_dist(pos_1, pos_2):
    return distance.euclidean(pos_1, pos_2)
    
def jaccard_dist(l_a, l_b):
    s_a = set(l_a)
    s_b = set(l_b)
    s_intersect = s_a.intersection(s_b)
    s_union = s_a.union(s_b)
    distance = float(len(s_intersect))/float(len(s_union))
    return distance
    
def dist_phone(a, b):
    
    a = a and re.subn('[^\d]', '',a)[0]
    b = b and re.subn('[^\d]', '',b)[0]
    return a!=b