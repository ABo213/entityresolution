from sklearn import tree
from sklearn import svm

def svm_model(y,X):
    clf = svm.SVC()
    clf.fit(X, y)
    return clf
def svm_predict(clf,Xt):
    y_new = clf.predict(Xt)
    return y_new[0]
    

def decisiontree_model(y, X):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    return clf
    
def decisiontree_predict(clf, Xt):
    y_new = clf.predict(Xt)
    return y_new[0]
