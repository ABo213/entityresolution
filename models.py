from sklearn import tree
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier

def svm_model(y,X):
    clf = svm.SVC(probability = True)
    clf.fit(X, y)
    return clf
def svm_predict(clf,Xt):
    y_new = clf.predict(Xt)
    y_prob = clf.predict_proba(Xt)
    return (y_new[0], y_prob[0][0])
    

def decisiontree_model(y, X):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)
    return clf
    
def decisiontree_predict(clf, Xt):
    y_new = clf.predict(Xt)
    y_prob = clf.predict_proba(Xt)
    return (y_new[0], y_prob)

def randomForest_model(y, X):
    clf = RandomForestClassifier()
    clf = clf.fit(X, y)
    return clf
    
def randomForest_predict(clf, Xt):
    y_new = clf.predict(Xt)
    return y_new[0]
    


