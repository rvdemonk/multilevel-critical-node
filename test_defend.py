from Protect import Protect
import networkx as nx
import matplotlib.pyplot as plt
from project.helpers import plot_graph, get_graph_data
from numpy.random import choice
from data import *


def test_defend_fence_example():
    Nodes = [i for i in range(1, 9)]
    Edges = [(2, 1), (2, 7), (7, 8), (8, 7), (2, 3), (3, 4), (4, 5), (5, 6)]
    Lambda = 2
    Infected_nodes = [2]
    Attack_vector = []
    for i in range(len(Nodes)):
        if (i + 1) in Infected_nodes:
            Attack_vector.append(1)
        else:
            Attack_vector.append(0)

    Saved, Protected = Protect(Nodes, Edges, Attack_vector, Lambda)
    print("Saved nodes: ", Saved)
    print("Number of nodes saved: ", len(Saved))


def test_defend_random_attack():
    # Graph parameters
    N = 20
    density = 5
    graph_num = 1

    # Model data
    Omega, Phi, Lambda = (3, 3, 3)
    nodes_, edges_ = get_graph_data(Numbers[graph_num], N, density, Omega, Phi, Lambda)
    rand_attack = list(choice([0, 1], size=(N,), p=[1 - (Phi / N), Phi / N]))

    saved, protected = Protect(nodes_, edges_, rand_attack, Lambda)
    print("Saved: ", saved)
    print("Protected: ", protected)


