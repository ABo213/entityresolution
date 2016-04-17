import os.path
DATA_DIR = 'data'
TEST_FILE0 = os.path.join(DATA_DIR, 'locu_test_hard.json')
TEST_FILE1 = os.path.join(DATA_DIR, 'foursquare_test_hard.json')
from data_reader import data_read
from pair_feature import generate_feature_list
import models
from test_bucket import *
def test_model(model):
    matches = []
    test_entity_a, test_entity_b = data_read(TEST_FILE0, TEST_FILE1)
    bucketB = Bucket(test_entity_b,0.025)
    for entity in test_entity_b:
        bucketB.addbucket(test_entity_b[entity])
    for entity0 in test_entity_a:
        #match_pair = []
        match_dict = {}
        if test_entity_a[entity0]["longitude"] and test_entity_a[entity0]["latitude"]:
            bucket_entities = bucketB.getbucket(test_entity_a[entity0]["longitude"],test_entity_a[entity0]["latitude"])
        else:
            bucket_entities = test_entity_b
        for entity1 in bucket_entities:
            features = generate_feature_list(test_entity_a[entity0],bucket_entities[entity1])
           # if features[-1] > 0.02:
           #     continue
            pred, prob = models.svm_predict(model,[features])
            if int(pred):
                match_dict[prob] = entity1
                #matches.append((entity0,entity1))
                #match_pair.append((entity0,entity1))
        #if len(match_pair)>1:
            #mulitmatch += match_pair
        if len(match_dict) > 0:
            match_prob = sorted(match_dict.keys(),reverse = True)
            #if len(match_dict) == 1:
            matches.append((entity0, match_dict[match_prob[0]]))
            #else:
            #    for i in range(2):
            #        matched_entity = match_dict[match_prob[i]]
            #        matches.append((entity0, matched_entity))
        
    
    f = open("output.csv",'w+')
    f.write("locu_id,foursquare_id\n")
    for i in matches:
        f.write(i[0]+","+i[1]+'\n')
    f.close()
    for i in range(len(matches)):
          e0, e1 = test_entity_a[matches[i][0]],test_entity_b[matches[i][1]]
          field_list = ["name","phone","street_address"]
          print "start"
          for field in field_list:
              print e0[field],"---", e1[field] 
          print "finish"
          
                
                
    
            
    

        
