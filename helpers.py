""" 
@lewisthompson

Utilities module for the MCNv2 algorithm.
"""
import os
import random
import matplotlib.pyplot as plt
from data import *
import pandas as pd
from datetime import datetime


RESULTS_PATH = "./results_v2/"


def get_timestamp():
    timestamp = str(datetime.now()).replace(" ", "_").split(".")[0]
    return timestamp.replace("/", "-").replace(":", "-")


def export_results(Results, graph_name):
    """
    Exports csv indexed by the number of the graph instance, 1-20
    """
    data = pd.DataFrame(Results, index=Numbers)
    timestamp = get_timestamp()
    path = RESULTS_PATH + f"{graph_name}/"
    if not os.path.exists(path):
        os.mkdir(path)
    data.to_csv(os.path.join(path, rf"{graph_name}_@{timestamp}.csv"))
    print("*" * 65 + f"\nExporting of {graph_name} results complete.\n" + "*" * 65)


def get_v2_result(N, density, Budgets):
    """
    Returns most recently exported csv of graph structure
    as a dataframe
    """
    graph_name = get_filename2(N, density, Budgets)
    if graph_name not in os.listdir(RESULTS_PATH):
        raise Exception(f"No results for graph {graph_name}")
    else:
        path = RESULTS_PATH + graph_name + "/"
        file = os.listdir(RESULTS_PATH + graph_name + "/")[-1]
        data = pd.read_csv(path + file)
    return data


def count_matching_solutions():
    """
    Exports a tabulated count of the number of objective solutions
    from MCNv2 that match those from the Baggio et al paper results.
    """
    MATCHES = {}
    for graph in os.listdir(RESULTS_PATH):
        path = RESULTS_PATH + graph + "/"
        file = os.listdir(RESULTS_PATH + graph + "/")[-1]
        data = pd.read_csv(path + file)
        MATCHES[graph] = sum(int(result) for result in data["sols match"])
    MATCHES.to_csv(RESULTS_PATH + "sol_check-" + get_timestamp() + ".csv")
    return MATCHES


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
                    if "optDA-AD" not in line:
                        stats["solution"] = int(line.split(" ")[0])
                if "#totTm" in line:
                    stats["time"] = float(line.split(" ")[0])
                if "#fail" in line:
                    stats["fail"] = "no" not in line.split(" ")[0]
                if "Z_dad" in line:
                    stats["Z_sol"] = eval(line.split(" = ")[1])
                if "Y_dad" in line:
                    stats["Y_sol"] = eval(line.split(" = ")[1])
                if "X_dad" in line:
                    stats["X_sol"] = eval(line.split(" = ")[1])
                if "lastADTm" in line:
                    stats["last AD time"] = float(line.split(" ")[0])
    else:
        raise Exception(f"no graph with name {name} in folder {folder+name}")
    return stats


def get_graph_data(number, N, density, Omega, Phi, Lambda):
    """
    Retrieves graph topology data from ./Instances/tables_MNC/
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


def extract_rndgraph_param(graph_name):
    """
    Given a name of a random graph instance, returns the parameters
    of the instance.
    """
    density = graph_name.split("-")[0][-2:]
    N = graph_name.split("-")[1].split("_")[0]
    BudgetsStrings = graph_name.split("_")[1].split("-")
    Budgets = [int(budget) for budget in BudgetsStrings]
    return N, density, Budgets
