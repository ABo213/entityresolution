import json
import re
import unicodedata


class Restaurant:

    attr_names = (
        'id', 'name', 'longitude', 'latitude', 'street_address', 'x', 'y'
    )

    def __init__(self, attr_dict):
        self.id = attr_dict['id']
        self.name = attr_dict['name']
        self.street_address = attr_dict['street_address']
        self.phone = attr_dict['phone']
        self.website = attr_dict['website']
        self.x = attr_dict['longitude']
        self.y = attr_dict['latitude']
        self.x = float(self.x or 'nan')
        self.y = float(self.y or 'nan')

    def __getitem__(self, item):
        if item in self.attr_names:
            return getattr(self, item)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{} @ ({:.3f}, {:.3f})'.format(repr(self.name), self.x, self.y)


class EntitiesPairData:
    """
    A pair of dicts of entities (using attribute 'id' as key).
    """
    def __init__(self, entity_seq0, entity_seq1):
        """
        initialize the data with sequences of entity instances
        :param entity_seq0: a sequence of one set of entities
        :param entity_seq1: a sequence of another set of entities
        """
        self.entity_dict0 = {e['id']: Restaurant(e) for e in entity_seq0}
        self.entity_dict1 = {e['id']: Restaurant(e) for e in entity_seq1}

    @classmethod
    def from_json(cls, file0_path, file1_path, clean=True):
        """
        load the data from two json files.
        :param file0_path: path to one file
        :param file1_path: path to another file
        :return: an instance of the class
        """
        with open(file0_path) as f0, open(file1_path) as f1:
            seq0, seq1 = json.load(f0), json.load(f1)
            if clean:
                for seq in (seq0, seq1):
                    for e in seq:
                        cls._clean_entity(e)
            data = cls(seq0, seq1)
        return data

    @staticmethod
    def _clean_entity(e):
        # keep only digits
        e['phone'] = re.subn(r'\D', '', str(e['phone']))[0]
        # remove non-English characters, convert to lowercase, and store as set
        name = unicodedata.normalize('NFD', e['name']).lower()
        name = re.subn('[^ a-z0-9]', '', name)[0]
        e['name'] = set(name.split())
        # convert to lowercase, use abbr., and remove non-English characters
        address = e['street_address'].lower()
        address = re.sub('west', 'w.', address)
        address = re.sub('east', 'e.', address)
        address = re.sub('south', 's.', address)
        address = re.sub('north', 'n.', address)
        address = re.sub('[^ .a-z0-9]', '', address)
        e['street_address'] = address
        # keep only the domain
        website = e['website']
        website = re.sub(r'(https?://)?(www.)?', '', website)
        website = re.sub(r'\..*', '', website)
        e['website'] = website


def load_matches_from_csv(csv_file):
    with open(csv_file) as f:
        f.readline()
        matches = [tuple(line.strip().split(',')) for line in f]
    return matches


