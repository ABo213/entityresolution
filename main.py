import os.path

from match import Matcher

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
TRAIN_FILE0 = os.path.join(DATA_DIR, 'locu_train_hard.json')
TRAIN_FILE1 = os.path.join(DATA_DIR, 'foursquare_train_hard.json')
TRAIN_MATCH_FILE = os.path.join(DATA_DIR, 'matches_train_hard.csv')
TEST_FILE0 = os.path.join(DATA_DIR, 'locu_test_hard.json')
TEST_FILE1 = os.path.join(DATA_DIR, 'foursquare_test_hard.json')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'matches_test_hard.csv')

m = Matcher()
m.fit(TRAIN_FILE0, TRAIN_FILE1, TRAIN_MATCH_FILE)
m.transform(TEST_FILE0, TEST_FILE1)
m.write(OUTPUT_FILE)