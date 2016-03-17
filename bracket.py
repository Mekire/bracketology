"""
Provided with a json file containing team seedings, simulates the
result of the NCAA tournament.  Winners are determined probabilistically
by the seedings.

For example, if two teams (a,b) play, the chance that team_a loses is
the seeding of team_a divided by the seeding of team_a + team_b.

With concrete numbers, the chance that a 1 seed loses to a 16 seed is
1/17 or approximately 5.9%.  The chance that a 10 seed loses to a 2 seed
is 10/12 or approximately 83%.
"""

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
    """
    Represents a single Node in our bracket tree.  After calc_data
    is run on the root node, the value of the node's data attribute
    will be the team that won in that round.
    """
    def __init__(self, depth=0, data=None, ):
        self.data = data
        self.left = None
        self.right = None
        self.depth = depth
        
    def calc_data(self):
        """
        Calulates (if necessary) and returns the value of the team
        placed in this Node.
        """
        if not self.data:
            self.data = self._predict_winner()
        return self.data
        
    def _predict_winner(self):
        """
        Returns the winner of the game played between the children.
        This requires that the children first play their games and
        as such recursively populates all nodes below this point in
        the tree.
        """
        team_1 = self.left.calc_data()
        team_2 = self.right.calc_data()
        normalization = team_1.seed + team_2.seed
        pick = random.random() > team_1.seed/normalization
        winner = team_1 if pick else team_2
        print("{} vs {}\n  Winner: {}\n".format(team_1, team_2, winner))
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
    print("Championship winner: {}\n".format(finals.data))
    
    
if __name__ == "__main__":
    main()
