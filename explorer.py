import json
import os.path

import distance

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

    def pair(self, i):
        id0, id1 = self.matches[i]
        return self.entities0[id0], self.entities1[id1]

    def difference(self, field='name', dis=lambda a, b: a != b,
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


if __name__ == '__main__':
    explorer = Explorer()
    explorer.difference('phone',dis=distance.dist_phone)
