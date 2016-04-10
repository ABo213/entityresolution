import json
import os.path

import distance
from generate_data  import generate_no_match
from pair_feature import generate_feature_list
import models  

DATA_DIR = 'data'
ENTITY_FILE0 = os.path.join(DATA_DIR, 'locu_train_hard.json')
ENTITY_FILE1 = os.path.join(DATA_DIR, 'foursquare_train_hard.json')
MATCH_FILE = os.path.join(DATA_DIR, 'matches_train_hard.csv')


class Explorer:
    def __init__(self, f0=ENTITY_FILE0, f1=ENTITY_FILE1, fm=MATCH_FILE):
        self.entities0 = {}
        for entity in json.load(open(f0)):
            id = entity['id']
            entity.pop('id')
            self.entities0[id] = entity
        self.entities1 = {}
        for entity in json.load(open(f1)):
            id = entity['id']
            entity.pop('id')
            self.entities1[id] = entity
        self.matches = []
        with open(fm) as f:
            f.readline()
            for line in f:
                self.matches.append(line.strip().split(','))
        self.nomatches = generate_no_match(self.entities0,self.entities1, self.matches, len(self.matches))

    def pair(self, i,ismatch=True):
        if ismatch is True: 
            id0, id1 = self.matches[i]
        else:
            id0, id1 = self.nomatches[i]
        return self.entities0[id0], self.entities1[id1]

    def difference(self, field='street_address', dis=lambda a, b: a != b,
                   threshold = 0.5, limit=None):
        count = 0
        for i in range(len(self.matches)):
            e0, e1 = self.pair(i)
            d = dis(e0[field], e1[field])
            if d > threshold:
                print('%d: (%f) %r ~ %r' % (i, d, e0[field], e1[field]))
                count += 1
                if limit is not None and count == limit:
                    break
    def trainscore(self):
        matches_list,match_label,nomatches_list,nomatch_label = [],[],[],[]
        #score_list,label = [],[]
        for i in range(len(self.matches)):
            e0, e1 = self.pair(i)
            score = generate_feature_list(e0,e1)
            matches_list.append(score)
            match_label.append('1')
           
        for i in range(len(self.nomatches)):
            e0, e1 = self.pair(i,False)
            score = generate_feature_list(e0,e1)
            nomatches_list.append(score)
            nomatch_label.append('0')
        train_label = match_label[:len(match_label)/2]+ nomatch_label[:len(nomatch_label)/2]
        test_label = match_label[len(match_label)/2:]+ nomatch_label[len(nomatch_label)/2:]
        train_list = matches_list[:len(matches_list)/2]+ nomatches_list[:len(nomatches_list)/2]
        test_list = matches_list[len(matches_list)/2:]+ nomatches_list[len(nomatches_list)/2:]
        ret = models.mysvm(train_label,train_list,test_label,test_list)
        print ret
        return ret
    def test():
        pass



if __name__ == '__main__':
    explorer = Explorer()
   # explorer.difference('street_address',dis=distance.dist_address)
    explorer.trainscore()
