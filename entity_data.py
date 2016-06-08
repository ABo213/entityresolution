import json
import unicodedata
import re
import os.path

import metrics

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
TRAIN_FILE0 = os.path.join(DATA_DIR, 'locu_train_hard.json')
TRAIN_FILE1 = os.path.join(DATA_DIR, 'foursquare_train_hard.json')
TRAIN_MATCH_FILE = os.path.join(DATA_DIR, 'matches_train_hard.csv')
TEST_FILE0 = os.path.join(DATA_DIR, 'locu_test_hard.json')
TEST_FILE1 = os.path.join(DATA_DIR, 'foursquare_test_hard.json')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'matches_test_hard.csv')


class EntityData:
    def __init__(self, f0, f1, fm=None):
        self.entities0 = {}
        for entity in json.load(open(f0)):
            self._read_entity(entity, self.entities0)
        self.entities1 = {}
        for entity in json.load(open(f1)):
            self._read_entity(entity, self.entities1)
        self.matches = []
        if fm is not None:
            with open(fm) as f:
                f.readline()
                for line in f:
                    self.matches.append(tuple(line.strip().split(',')))
        self.preprocess()

    def preprocess(self):
        for e in self.entities0.values():
            self._process_entity(e)
        for e in self.entities1.values():
            self._process_entity(e)

    @staticmethod
    def _process_entity(e):
        e['phone'] = re.subn(r'\D', '', e['phone'])[0] if e['phone'] else None

        e['postal_code'] = e['postal_code'] if e['postal_code'][:5] else '     '

        name = unicodedata.normalize('NFKD', e['name']).lower()
        name = re.subn('[^ a-z0-9]', '', name)[0]
        e['name'] = set(name.split()) or None

        address = e['street_address'].lower()
        address = re.sub('west', 'w.', address)
        address = re.sub('east', 'e.', address)
        address = re.sub('south', 's.', address)
        address = re.sub('north', 'n.', address)
        address = re.sub('[^ a-z0-9]', '', address)
        e['street_address'] = address or None

        website = e['website']
        website = re.sub(r'(https?://)?(www.)?', '', website)
        website = re.sub(r'\..*', '', website)
        e['website'] = website or None

    @staticmethod
    def _read_entity(e, entities_dict):
        id = e.pop('id')
        e['longitude'] = e['longitude'] and float(e['longitude'])
        e['latitude'] = e['latitude'] and float(e['latitude'])
        entities_dict[id] = e


class Explorer:
    def __init__(self, trainf0=TRAIN_FILE0, trainf1=TRAIN_FILE1,
                 trainfm=TRAIN_MATCH_FILE, testf0=TEST_FILE0,
                 testf1=TEST_FILE1):
        self.train_data = EntityData(trainf0, trainf1, trainfm)
        self.test_data = EntityData(testf0, testf1)

    def difference(self, field='name', dis=lambda a, b: a != b,
                   threshold=0.5, limit=None):
        ret = []
        count = 0
        for i in range(len(self.train_data.matches)):
            e0, e1 = self._train_match_pair(i)
            if metrics.isna_dist(e0[field], e1[field]): continue
            d = dis(e0[field], e1[field])
            if d > threshold:
                ret.append(i)
                print('%3d: (%.2f) %r ~ %r' % (i, d, e0[field], e1[field]))
                count += 1
                if limit is not None and count == limit:
                    break
        return ret

    def _train_match_pair(self, i):
        id0, id1 = self.train_data.matches[i]
        return self.train_data.entities0[id0], self.train_data.entities1[id1]

    def print_pair(self, i):
        e0, e1 = self._train_match_pair(i)
        for field in e0:
            print('%s: %r ~ %r' % (field, e0[field], e1[field]))