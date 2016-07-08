import os.path

from experiment import Explorer
from match import Matcher

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
TRAIN_FILE0 = os.path.join(DATA_DIR, 'locu_train_hard.json')
TRAIN_FILE1 = os.path.join(DATA_DIR, 'foursquare_train_hard.json')
TRAIN_MATCH_FILE = os.path.join(DATA_DIR, 'matches_train_hard.csv')
TEST_FILE0 = os.path.join(DATA_DIR, 'locu_test_hard.json')
TEST_FILE1 = os.path.join(DATA_DIR, 'foursquare_test_hard.json')
TEST_MATCH_FILE = os.path.join(DATA_DIR, 'matches_test_hard.csv')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'result.csv')


def compare_results(result_file=OUTPUT_FILE, baseline_file=TEST_MATCH_FILE):
    with open(result_file) as f:
        f.readline()
        result_set = set(f)
    with open(baseline_file) as f:
        f.readline()
        baseline_set = set(f)
    print(len(result_set), len(baseline_set), len(result_set & baseline_set))


def main():
    m = Matcher()
    m.fit(TRAIN_FILE0, TRAIN_FILE1, TRAIN_MATCH_FILE)
    m.transform(TEST_FILE0, TEST_FILE1)
    m.write(OUTPUT_FILE)


explorer = Explorer(TRAIN_FILE0, TRAIN_FILE1, TRAIN_MATCH_FILE)
