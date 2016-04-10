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
    return float(pre[-1])/(len(word1)+len(word2)-pre[-1])
    
def euclidean_dist(pos_1, pos_2):
    return distance.euclidean(pos_1, pos_2)
    
def jaccard_dist(l_a, l_b):
    s_a = set(l_a)
    s_b = set(l_b)
    s_intersect = s_a.intersection(s_b)
    s_union = s_a.union(s_b)
    distance = 1 - float(len(s_intersect))/float(len(s_union))
    return distance
    
def dist_phone(a, b):
    
    a = a and re.subn('[^\d]', '',a)[0]
    b = b and re.subn('[^\d]', '',b)[0]
    return 0.5 * (not a or not b) or float(a!=b)
    
def dist_address(a, b):
    sub_list =[
        ('West', 'W.'),
        ('South', 'S.'),
        ('East', 'E.'),
        ('(?<=[\d])th',''),
        ('St.',''),
        ('Ave.','')
    ]
    for i in sub_list:
         a = a and re.subn(i[0], i[1],a)[0]
         b = b and re.subn(i[0], i[1],b)[0]
    return  0.5 * (not a or not b) or float(a!=b)
  
def my_jaccard_dist(name_a, name_b):
    name_a = name_a.lower()
    name_b = name_b.lower()
    name_a_list = re.subn('[^\w]',' ',name_a)[0].split()
    name_b_list = re.subn('[^\w]',' ',name_b)[0].split()
    name_jaccard = jaccard_dist(name_a_list, name_b_list)
    return name_jaccard  
    
