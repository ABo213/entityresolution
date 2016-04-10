from explorer import Explorer
from generate_data import generate_no_match
def main():
    explorer = Explorer()
    entities_a = explorer.entities0
    entities_b = explorer.entities1
    matches_list = explorer.matches
    no_matches = generate_no_match(entities_a,entities_b, matches_list, len(matches_list))
    print no_matches
    
main()    
    
    
