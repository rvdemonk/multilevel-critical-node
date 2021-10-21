from DefendAttackDefend import MCN
from helpers import get_graph_data, get_paper_stats
import pytest
from data import graph_base_name, Ns, BudgetSet, Numbers, Density

Omega, Phi, Lambda = 2, 2, 2

nodes, edges = get_graph_data(Numbers[0], Ns[0], Density[0], Omega, Phi, Lambda)

stats = get_paper_stats(Numbers[0], Ns[0], Density[0], Omega, Phi, Lambda)

output = MCN(nodes, edges, Omega, Phi, Lambda)

print(type(output["total_time"]))
for key in output.keys():
    print(f"{key.upper()} : {output[key]}")


def test_MCN_single(N, density, Budgets):
    Omega, Phi, Lambda = Budgets[0], Budgets[1], Budgets[2]
    Results = []
    for graph in Numbers:
        nodes, edge = get_graph_data(graph, N, density, Omega, Phi, Lambda)
        solutions = get_paper_stats(graph, N, density, Omega, Phi, Lambda)
