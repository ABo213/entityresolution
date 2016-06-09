import metrics
from entity_data import EntitiesPairData, load_matches_from_csv


class Explorer:
    """
    an instance of EntitiesPairData optionally with a list of matches between
    them.
    """
    def __init__(self, entity_file0, entity_file1, match_file):

        self.data = EntitiesPairData.from_json(entity_file0, entity_file1)
        self.matches = load_matches_from_csv(match_file)

    def __getitem__(self, i):
        id0, id1 = self.matches[i]
        return self.data.entity_dict0[id0], self.data.entity_dict1[id1]

    def __iter__(self):
        for id0, id1 in self.matches:
            yield self.data.entity_dict0[id0], self.data.entity_dict1[id1]

    def unmatched_attr_iter(self, attr='name', dist=metrics.ne, threshold=0.5):
        for e0, e1 in self:
            a0, a1 = getattr(e0, attr), getattr(e1, attr)
            if metrics.has_na(a0, a1):
                continue
            d = dist(a0, a1)
            if d > threshold:
                yield e0, e1

    def print_pair(self, i):
        e0, e1 = self[i]
        print('name: {} ~ {}'.format(e0.name, e1.name))
        print('coordinate: ({}, {}) ~ ({}, {})'.format(
            e0.x, e0.y, e1.x, e1.y
        ))
        print('address: {} ~ {}'.format(e0.street_address, e1.street_address))
        print('phone: {} ~ {}'.format(e0.phone, e1.phone))
        print('website: {} ~ {}'.format(e0.website, e1.website))