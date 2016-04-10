# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 15:52:25 2016

@author: huisu
"""
from sklearn import svm

def mysvm(y,X,yt,Xt):
    clf = svm.SVC()
    clf.fit(X, y)
    y_new = clf.predict(Xt)
    count = 0
    for i in range(len(y_new)):
        if y_new[i] == yt[i]:
            count+= 1
    return float(count)/len(y_new)
    
    
