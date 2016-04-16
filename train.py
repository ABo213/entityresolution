import json
import os.path
from generate_data  import generate_no_match
from pair_feature import generate_feature_list
import models  

DATA_DIR = 'data'
TRAIN_FILE0 = os.path.join(DATA_DIR, 'locu_train_hard.json')
TRAIN_FILE1 = os.path.join(DATA_DIR, 'foursquare_train_hard.json')
MATCH_FILE = os.path.join(DATA_DIR, 'matches_train_hard.csv')
from data_reader import data_read

def train_model():
        skip_set = set([90, 178, 182, 215, 285, 286])
        train_entity_a, train_entity_b = data_read(TRAIN_FILE0, TRAIN_FILE1)
        matches = []
        with open(MATCH_FILE) as f:
            f.readline()
            for line in f:
                matches.append(line.strip().split(','))
        nomatches = generate_no_match(train_entity_a, train_entity_b, matches,len(matches))
        matches_list,match_label,nomatches_list,nomatch_label = [],[],[],[]
        for i in range(len(matches)):
            if i in skip_set:
                continue
            e0, e1 = train_entity_a[matches[i][0]],train_entity_b[matches[i][1]]
            score = generate_feature_list(e0,e1)
            matches_list.append(score)
            match_label.append('1')
           
        for i in range(len(nomatches)):
            e0, e1 = train_entity_a[nomatches[i][0]],train_entity_b[nomatches[i][1]]
            score = generate_feature_list(e0,e1)
            nomatches_list.append(score)
            nomatch_label.append('0')
        train_label = match_label + nomatch_label
        train_list = matches_list + nomatches_list
        model = models.svm_model(train_label,train_list)
        #model = models.decisiontree_model(train_label,train_list)
        #model = models.randomForest_model(train_label,train_list)
        return model
    
    