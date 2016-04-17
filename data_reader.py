import json

def data_read(f0, f1):
    entities0 = {}
    for entity in json.load(open(f0)):
        id = entity['id']
        entity.pop('id')
        entities0[id] = entity
    entities1 = {}
    for entity in json.load(open(f1)):
        id = entity['id']
       # entity.pop('id')
        entities1[id] = entity
    return(entities0, entities1)
        