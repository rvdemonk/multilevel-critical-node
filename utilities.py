from helpers import *

def get_high_traffic_nodes(Nodes, Arcs, Phi):
    EdgeCount = {v: 0 for v in Nodes}
    for arc in Arcs:
        EdgeCount[arc[0]] += 1
        EdgeCount[arc[1]] += 1
    Scores = [(EdgeCount[v],v) for v in EdgeCount]
    Scores.sort(reverse=True)
    crit_nodes = [score[1] for score in Scores]
    return crit_nodes
        