from __future__ import print_function, division

import json
import random


REGIONS = ["SOUTH", "WEST", "EAST", "MIDWEST"]
ROUND_1_ORDER = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
with open("bracket.json") as infile:
    SEEDS = json.load(infile)


class Team(object):
    """
    A basic class representing a team.
    Instances of this class are stored in the Node.data elements
    of the generated tree.
    """
    def __init__(self, name, seed, region):
        self.name = name
        self.seed = seed
        self.region = region
        
    def __repr__(self):
        return "{seed}.{name}".format(**vars(self))


class Node(object):
    def __init__(self, depth=0, data=None, ):
        self.data = data
        self.left = None
        self.right = None
        self.depth = depth
        
    def calc_data(self):
        self.data = self._predict_winner()
        
    def _predict_winner(self):
        if not self.left.data and not self.right.data:
            self.left.calc_data()
            self.right.calc_data()
        team_1, team_2 = self.left.data, self.right.data
        normalization = team_1.seed + team_2.seed
        pick = random.random() > team_1.seed/normalization
        winner = team_1 if pick else team_2
        print("{} vs {}\n    Winner: {}".format(team_1, team_2, winner))
        return winner        


def get_empty_bracket(root, round_1, depth=1):
    """
    Generates a binary tree.  The Node.data element is set to
    None for all Nodes except for the leaves.  
    The leaf data is taken from an ordered list of first round teams.
    """
    if depth < 6:
        root.left = get_empty_bracket(Node(depth), round_1, depth+1)
        root.right = get_empty_bracket(Node(depth), round_1, depth+1)
    else:
        root.left = Node(depth, round_1.pop(0))
        root.right = Node(depth, round_1.pop(0))
    return root
        

def make_teams():
    """
    Iterate through the loaded json data and create a list of
    Team instances.  The ordering of the list is important as it 
    determines how teams are placed in the leaves of the tree.
    """
    teams = []
    for region in REGIONS:
        for seed in ROUND_1_ORDER:
            name = SEEDS[region][str(seed)]
            teams.append(Team(name, int(seed), region))
    return teams
         
        
def main():
    teams = make_teams()
    finals = Node()
    get_empty_bracket(finals, teams)
    finals.calc_data()
    print("Championship winner: {}".format(finals.data))
    
    
if __name__ == "__main__":
    main()
