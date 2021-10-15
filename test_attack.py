from data import *
from AttackDefend import AP
from helpers import get_graph_data


def test_AP_functionality(density, N, number, Omega, Phi, Lambda):

    Nodes, Edges = get_graph_data(number, N, density, Omega, Phi, Lambda)
    target = 3
    I, status = AP(Nodes, Edges, Phi, Lambda, target)

    return I, status


I, status = test_AP_functionality(5, 20, "001", 2,2,2)
Infected_nodes = [i+1 for i in range(len(I)) if I[i] > 0.9]
print(I)
print(Infected_nodes)
print("Status: ", status)
