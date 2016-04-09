# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 15:55:42 2016

@author: Lapland
"""
def jaccard_dist(l_a, l_b):
    s_a = set(l_a)
    s_b = set(l_b)
    s_intersect = s_a.intersection(s_b)
    s_union = s_a.union(s_b)
    distance = float(len(s_intersect))/float(len(s_union))
    return distance
    
