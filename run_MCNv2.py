"""
@lewisthompson

Central command module for running the MCNv2 algorithm on the provided
rndgraph instances located in ./Instances/tables_MNC/
"""

from pandas.core.indexing import need_slice
from ProtectAttackDefend import MCNv2
from helpers import *
from data import graph_base_name, Ns, Density, BudgetSet, Numbers
import pandas as pd
from datetime import datetime
import os
import signal


def run_MCNv2_single(N, number, density, Budgets):
    """
    Runs the MCNv2 algorithm on a single instance of a rndgrpah structure.
    Instance number specified by number parameter.
    """
    Omega, Phi, Lambda = Budgets[0], Budgets[1], Budgets[2]
    graph_name = get_filename(N, density, Omega, Phi, Lambda)
    nodes, edges = get_graph_data(number, N, density, Omega, Phi, Lambda)
    results = {}
    results["graph name"] = graph_name
    print(f"\nTesting {graph_name}_{number}")

    # try first, except timeout
    try:
        OUTPUTV2 = MCNv2(nodes, edges, Omega, Phi, Lambda)
    except:
        # MCNv2 timed out
        OUTPUTV2 = {"fail": True}

    # get paper results for this instance
    PAPER = get_paper_stats(number, N, density, Omega, Phi, Lambda)
    # detect if the paper experiment failed on this instance
    try:
        results["og fail"] = PAPER["fail"]
    except KeyError:
        PAPER["fail"] = True

    if not PAPER["fail"] and not OUTPUTV2["fail"]:
        results["sols match"] = PAPER["solution"] == OUTPUTV2["objVal"]
        results["v2 faster"] = OUTPUTV2["total time"] < PAPER["time"]
        results["og time"] = PAPER["time"]
        results["v2 time"] = OUTPUTV2["total time"]
        results["time diff"] = results["v2 time"] - results["og time"]
        results["og obj"] = PAPER["solution"]
        results["v2 obj"] = OUTPUTV2["objVal"]
        results["og X"] = PAPER["X_sol"]
        results["v2 X"] = OUTPUTV2["X_sol"]
        results["og Y"] = PAPER["Y_sol"]
        results["v2 Y"] = OUTPUTV2["Y_sol"]
        results["og Z"] = PAPER["Z_sol"]
        results["v2 Z"] = OUTPUTV2["Z_sol"]
        # results["og last AD Tm"] = PAPER["last_AD_time"]
    return results


def run_MCNv2_all_nums(N, density, Budgets, timelimit=False):
    """
    Runs MCNv2 on all 20 instances of a given rndgraph topology and
    budget set.
    # timelimit parameter unused and broken - use timeout decorator
    on MCNv2 function.
    """
    Data = []
    Timeouts = []
    if not timelimit:
        for num in Numbers:
            print(f"\n--> TESTING GRAPH {num}")
            results = run_MCNv2_single(N, num, density, Budgets)
            Data.append(results)
    else:  ## broken
        signal.signal(signal.SIGALRM, timeout_handler)
        for num in Numbers:
            print(f"\n--> TESTING GRAPH {num}")
            signal.alarm(timelimit)
            try:
                results = run_MCNv2_single(N, num, density, Budgets)
                Data.append(results)
            except Exception:
                continue
    graphname = get_filename2(N, density, Budgets)
    export_results(Data, graphname)
    return Data, Timeouts


def run_MCNv2_budgets(Budgets, timelimit=False):
    # tests against all rndgraph instances with the given budget
    TIMEOUTS = {}
    for N in Ns:
        for dens in Density:
            graph_name = get_filename2(N, dens, Budgets)
            path = f"./Instances/tables_MNC/{graph_name}"
            if os.path.exists(path):
                Data, timeouts = run_MCNv2_all_nums(
                    N, dens, Budgets, timelimit=timelimit
                )
                TIMEOUTS[graph_name] = timeouts
    return TIMEOUTS


def run_MCNv2_density(density):
    """
    Runs MCNv2 on all topologies and budget sets with the given density.
    """
    for N in Ns:
        for Budgets in BudgetSet:
            graph_name = get_filename2(N, density, Budgets)
            path = f"./Instances/tables_MNC/{graph_name}"
            if os.path.exists(path):
                Data, timeouts = run_MCNv2_all_nums(
                    N, density, Budgets, timelimit=False
                )
    return Data


# ------------------------------------------------------------------------ #


def main():
    ## this would run the MCNv2 on all graph instances with 2,2,2 budget
    # run_MCNv2_budgets([2,2,2])

    ## this would run MCNv2 on all instances with a density of 5
    # run_MCNv2_density(5)

    run_MCNv2_all_nums(20, 5, [1, 1, 1])


if __name__ == "__main__":
    main()
