import json
import os.path
#
# import matplotlib.pyplot as plt

import distance

DATA_DIR = 'data'
ENTITY_FILE0 = os.path.join(DATA_DIR, 'locu_test_hard.json')
ENTITY_FILE1 = os.path.join(DATA_DIR, 'foursquare_test_hard.json')
MATCH_FILE = os.path.join(DATA_DIR, 'output.csv')


class Explorer:
    def __init__(self, f0=ENTITY_FILE0, f1=ENTITY_FILE1, fm=MATCH_FILE):
        self.entities0 = {}
        for entity in json.load(open(f0)):
            self._read_entity(entity, self.entities0)
        self.entities1 = {}
        for entity in json.load(open(f1)):
            self._read_entity(entity, self.entities1)
        self.matches = []
        with open(fm) as f:
            f.readline()
            for line in f:
                self.matches.append(line.strip().split(','))

    @staticmethod
    def _read_entity(entity, entities_dict):
        id = entity['id']
        entity['location'] = (entity['longitude'], entity['latitude'])
        entity.pop('longitude')
        entity.pop('latitude')
        entity.pop('id')
        entities_dict[id] = entity

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

    def field(self, filter=lambda x: True):
        pass

    # def map(self):
    #     x, y = zip(*(e['location'] for e in self.entities0.values()))
    #     plt.scatter(x, y)
    #     plt.xlim((-74.1, -73.9))
    #     plt.ylim((40.6, 40.9))
    #     plt.show()

    def pair(self, i):
        id0, id1 = self.matches[i]
        return self.entities0[id0], self.entities1[id1]

    def print_pair(self, i):
        e0, e1 = self.pair(i)
        for field in e0:
            print('%s: %r ~ %r' % (field, e0[field], e1[field]))



if __name__ == '__main__':
    explorer = Explorer()
    explorer.difference('street_address', dis=distance.fuzzy_address,threshold = 0)
    # explorer.map()
