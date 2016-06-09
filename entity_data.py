import json


class Restaurant:
    attr_names = (
        'id', 'name', 'longitude', 'latitude', 'street_address', 'phone',
        'website'
    )

    def __init__(self, attr_dict):
        self.id = attr_dict['id']
        self.name = attr_dict.get('name')
        self.street_address = attr_dict.get('street_address')
        self.phone = attr_dict.get('phone')
        self.website = attr_dict.get('website')
        self.x = attr_dict.get('longitude')
        self.y = attr_dict.get('latitude')
        self.x = float(self.x) if self.x else None
        self.y = float(self.y) if self.y else None

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
    def from_json(cls, file0_path, file1_path):
        """
        load the data from two json files.
        :param file0_path: path to one file
        :param file1_path: path to another file
        :return: an instance of the class
        """
        with open(file0_path) as f0, open(file1_path) as f1:
            data = cls(json.load(f0), json.load(f1))
        return data


    # def preprocess(self):
    #     for e in self.entities0.values():
    #         self._process_entity(e)
    #     for e in self.entities1.values():
    #         self._process_entity(e)

    # @staticmethod
    # def _process_entity(e):
    #     e['phone'] = re.subn(r'\D', '', e['phone'])[0] if e['phone'] else None
    #
    #     e['postal_code'] = e['postal_code'] if e['postal_code'][:5] else '     '
    #
    #     name = unicodedata.normalize('NFKD', e['name']).lower()
    #     name = re.subn('[^ a-z0-9]', '', name)[0]
    #     e['name'] = set(name.split()) or None
    #
    #     address = e['street_address'].lower()
    #     address = re.sub('west', 'w.', address)
    #     address = re.sub('east', 'e.', address)
    #     address = re.sub('south', 's.', address)
    #     address = re.sub('north', 'n.', address)
    #     address = re.sub('[^ a-z0-9]', '', address)
    #     e['street_address'] = address or None
    #
    #     website = e['website']
    #     website = re.sub(r'(https?://)?(www.)?', '', website)
    #     website = re.sub(r'\..*', '', website)
    #     e['website'] = website or None
    #
    # @staticmethod
    # def _read_entity(e, entities_dict):
    #     id = e.pop('id')
    #     e['longitude'] = e['longitude'] and float(e['longitude'])
    #     e['latitude'] = e['latitude'] and float(e['latitude'])
    #     entities_dict[id] = e


def load_matches_from_csv(csv_file):
    with open(csv_file) as f:
        f.readline()
        matches = [tuple(line.strip().split(',')) for line in f]
    return matches


