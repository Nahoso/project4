#! /usr/bin/env python3
################################################################################
#
# Implementation of the TSP problem class
#
################################################################################
from search import *
import re
import sys
import os


#################
# Problem class #
#################
class TSP(Problem):

    """TSP skeleton. Fill in the gaps."""
    def __init__(self, instance):
        # Read data
        lines = [line.rstrip('\n') for line in open(instance)]
        self.n = int(lines[0])
        self.cities = []
        for i in range(1, self.n + 1):
            part = lines[i].split()
            self.cities.append((float(part[0]), float(part[1])))

        def dist(city1, city2):
            return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

        # Compute distance matrix
        self.dist = []
        for i in range(self.n):
            dist_ = []
            for j in range(self.n):
                dist_.append(dist(self.cities[i], self.cities[j]))
            self.dist.append(dist_)

        # Dummy initial solution. Change it to build your initial solution.
        # self.initial = list(range(self.n))

        # Greedy initial solution
        self.initial = [0]  # Adding first city

        visitable = list(range(self.n))  # Cities to visit
        i = 0 # First city is 0
        visitable.remove(i) # Retirer i de visitable
        print(visitable)
        while visitable:
            nearest = visitable[0] # initialiser a la premiere ville la plus proche
            for j in visitable:
                if self.dist[j][i] < self.dist[j][nearest]: # nouvelle ville plus proche
                    nearest = j
            self.initial.append(nearest) # add nearest to the list
            i = nearest # new city
            visitable.remove(nearest) # remove nearest from cities to visit


    def successor(self, state):
        """
        For successor(self, state) function, you should return a list of (act, succ) 
        where the state succ is obtained by apply the action act, in this case, act = (i, j) 
        consists in applying 2-opt swap on the two edges (state[i-1], state[i]) and  (state[j], state[j+1]). 
        (state here is an ordered sequence of visited cities)

        For example, consider the following state:
        state = [7, 2, 1, 5, 4, 3, 0, 6]
        One possible successor of this state could be ((1,5), succ), with:
        succ = [7, 3, 4, 5, 1, 2, 0, 6]
        Since act = (1, 5), it means that the two edges (7, 2) and (3,0) have been swapped in succ. 
        You should try to visualize this example, it will be more easier to see.
        You should reverse path between index i and index j to preserve other edges.
        """
        print("successor")
        new_state = state[:] # copy of the state
        reversed_state = list(reversed(new_state))
        for i in range(len(state)):
            for j in range(len(state)):
                if i != j-1 and i!= j+1 : # no city in common
                    list(reversed(state[i:j])) # reversed part of the list
                    new_state = state[:i] # start of the list identical
                    new_state.extend(reversed_state) # reversed middle list
                    new_state.extend(state[j:]) # end of the list indentical
                    yield((i,j),new_state)



    def value(self, state):
        """
        The value function must return an integer value
        representing the length of TSP route.
        """
        i=-1
        total_cost = 0
        for _ in range(len(state)):
            city_a = state[i]
            city_b = state[i+1]
            total_cost = total_cost+ self.dist[city_a][city_b]
            i=i+1
        return total_cost


def max_node(list_node):
    print(2)
    best = list_node[0]
    for current in list_node:
        print(3)
        if current.value() > best.value():
            best = current
    return best

def max_first_node(list_node, nb_nodes): # min 1 node
    best_list = [list_node[:nb_nodes]] # place les nb_node premiers dans la liste
    for current in list_node:
        for state in best_list:
            if current.value() > state.value():
                best_list.remove(state) # enleve de la liste l'ancien
                best_list.append(current) # ajoute à la liste le nouveau
    return best_list

#################
# Local Search #
#################
def maxvalue(problem, limit=100, callback=None):
    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        print(1)
        if callback is not None:
            callback(current)
        current = max_node(list(current.expand()))
        if current.value() > best.value():
            best = current
    return best


def randomized_maxvalue(problem, limit=100, callback=None):
    # use this line to submit on INGInious
    # random.seed(12)

    current = LSNode(problem, problem.initial, 0)
    best = current
    for step in range(limit):
        if callback is not None:
            callback(current)
        max_5_nodes=max_first_node(list(current.expand(),5))
        current = random.choice(max_5_nodes)
        if current.value() > best.value():
            best = current
    return best


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "tsp_instance", file=sys.stderr)
        exit(1)

    tsp = TSP(sys.argv[1])
    node = maxvalue(tsp, 100)

    # prepare output data to printout
    output_data = '%.2f' % tsp.value(tsp.initial) + '\n'
    output_data += ' '.join(map(str, tsp.initial)) + '\n'
    output_data += "%.2f" % node.value() + '\n'
    output_data += ' '.join(map(str, node.state)) + '\n'
    print(output_data)
