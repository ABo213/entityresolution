from collections import defaultdict

import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import Imputer

import entity_data
import metrics


def pair_filter(a, b):
    return metrics.geo_dist(a['longitude'], b['longitude']) < 0.01 and \
           metrics.geo_dist(a['latitude'], b['latitude']) < 0.01

feature_functions = [
    ('phone', metrics.ne),
    ('name', metrics.jaccard_dist),
    ('street_address', metrics.edit_dist),
    ('website', metrics.edit_dist),
    ('longitude', metrics.num1p_dist),
    ('latitude', metrics.num1p_dist)
]


def extract(a, b, ffs = feature_functions):
    return [func(a[field], b[field]) if not metrics.has_na(a[field], b[
        field]) else float('nan') for field, func in ffs]


class Trainer:
    def __init__(self, f0, f1, fm, filter=pair_filter, extracter=extract):
        data = entity_data.EntitiesPairData(f0, f1, fm)
        self.eset0 = data.entities0
        self.eset1 = data.entities1
        self.eset1bucket = None
        self.matches = set(data.matches)
        self.filter = filter
        self.extracter=extracter
        self.x = None
        self.y = None
        self.ids = None
        self.classifier = SVC(kernel='linear')

    def bucketify_e1(self):
        buckets = defaultdict(dict)
        for id, e in self.eset1.items():
            if e['longitude'] is None or e['latitude'] is None: continue
            key = (int(e['longitude'] * 100), int(e['latitude'] * 100))
            buckets[key][id] = e
        self.eset1bucket = dict(buckets)

    def _pair_generator_from_bucket(self):
        self.bucketify_e1()
        for id0, e0 in self.eset0.items():
            if e0['longitude'] is None or e0['latitude'] is None: continue
            x, y = (int(e0['longitude'] * 100), int(e0['latitude'] * 100))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for id1, e1 in self.eset1bucket.get((x + dx, y + dy), {}).items():
                        if self.filter(e0, e1):
                            yield id0, id1

    def _pair_generator(self):
        for id0, e0 in self.eset0.items():
            for id1, e1 in self.eset1.items():
                if self.filter(e0, e1):
                    yield id0, id1

    def generate_train_data(self):
        x, y, ids = [], [], []
        cnt = 0
        for pair in self._pair_generator_from_bucket():
            x.append(self.extracter(self.eset0[pair[0]], self.eset1[pair[1]]))
            y.append(pair in self.matches)
            ids.append(pair)
            cnt += 1
            # if cnt == 100: break
        self.x = Imputer().fit_transform(np.matrix(x))
        self.y = np.array(y)
        self.ids = ids

    def train(self):
        self.classifier.fit(self.x, self.y)

    def write(self, file_name):
        with open(file_name, 'w') as f:
            f.write('locu_id,foursquare_id\n')
            for pair in self._pair_generator():
                if pair not in self.matches:
                    f.write('%s,%s\n' % pair)


class Matcher:
    def __init__(self):
        self.classifier = None
        self.x = None
        self.y = None
        self.ids = None
        self.predict = None

    def fit(self, f0, f1, mf):
        trainer = Trainer(f0, f1, mf)
        trainer.generate_train_data()
        trainer.train()
        self.classifier = trainer.classifier

    def transform(self, f0, f1):
        trainer = Trainer(f0, f1, None)
        trainer.generate_train_data()
        self.x = trainer.x
        self.y = trainer.y
        self.ids = trainer.ids
        self.predict = self.classifier.predict(self.x)

    def write(self, file_name):
        with open(file_name, 'w') as f:
            f.write('locu_id,foursquare_id\n')
            for m, pair in zip(self.predict, self.ids):
                if m:
                    f.write('%s,%s\n' % pair)



