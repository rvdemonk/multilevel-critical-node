import os
import random
import matplotlib.pyplot as plt
import networkx as nx
from data import *


def get_filename(N, density, Omega, Phi, Lambda):
    # takes budgets as three integers
    density = f"0{density}" if int(density) < 10 else density
    return f"rndgraph{density}-{N}_{Omega}-{Phi}-{Lambda}"

def get_filename2(N, density, Budgets):
    # Takes bugdets as a list instead of three integers
    density = f"0{density}" if int(density) < 10 else density
    Omega, Phi, Lambda = Budgets
    return f"rndgraph{density}-{N}_{Omega}-{Phi}-{Lambda}"
    

def get_paper_stats(number, N, density, Omega, Phi, Lambda):
    """
    Retrieves the optimal solutions from the published data.
    """
    stats = {}
    name = get_filename(N, density, Omega, Phi, Lambda)
    if [Omega, Phi, Lambda] not in BudgetSet:
        raise Exception("No such budget combination")
    if os.path.isfile(folder + name + "/" + name + "_" + number):
        with open(folder + name + "/" + name + "_" + number) as searchfile:
            for line in searchfile:
                if "#opt" in line:
                    stats["solution"] = int(line.split(" ")[0])
                if "#totTm" in line:
                    stats["time"] = float(line.split(" ")[0])
                if "#fail" in line:
                    stats["fail"] = line.split(" ")[0]
                if "Z_dad" in line:
                    stats["Z_sol"] = eval(line.split(" = ")[1])
                if "Y_dad" in line:
                    stats["Y_sol"] = eval(line.split(" = ")[1])
                if "X_dad" in line:
                    stats["X_sol"] = eval(line.split(" = ")[1])
    else:
        raise Exception(f"no graph with name {name} in folder {folder+name}")
    return stats


def get_graph_data(number, N, density, Omega, Phi, Lambda):
    """
    Retrieves graph data from ./Instances/tables_MNC/
    Returns V, A
    """
    name = get_filename(N, density, Omega, Phi, Lambda)
    if os.path.isfile(folder + name + "/" + name + "_" + number):
        V = range(1, N + 1)
        with open(folder + name + "/" + name + "_" + number) as searchfile:
            for line in searchfile:
                if "A =" in line:
                    A = eval(line[4:])
    else:
        raise Exception(f"no graph with name {name} in folder {folder+name}")
    return V, A


def plot_graph(nodes, edges, infected=None, saved=None):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    nx.draw(G, with_labels=True, font_weight="bold")
    plt.show()


def get_mcn_results(N, density, Budgets):
    """
    Returns the results of a rnd graph instance for all numbers of that
    graph as a pandas dataframe, indexed by the graph instance number (1-20)
    """
    graphname = get_filename2(N, density)
