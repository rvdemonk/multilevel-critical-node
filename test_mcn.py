from pandas.core.indexing import need_slice
from DefendAttackDefend2 import MCN
from helpers import get_graph_data, get_paper_stats, get_filename, get_filename2
from data import graph_base_name, Ns, Density, BudgetSet, Numbers
import pandas as pd
from datetime import datetime
import os
import signal


RESULTS_PATH = "./results21/"

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
    print("*" * 65 + f"\Exporting of {graph_name} results complete.\n" + "*" * 65)


def run_MCN_single(N, number, density, Budgets):
    Omega, Phi, Lambda = Budgets[0], Budgets[1], Budgets[2]
    graph_name = get_filename(N, density, Omega, Phi, Lambda)
    nodes, edges = get_graph_data(number, N, density, Omega, Phi, Lambda)
    
    print(f"\nTesting {graph_name}_{number}")
    OUTPUTV2 =  MCN(nodes, edges, Omega, Phi, Lambda)

    PAPER = get_paper_stats(number, N, density, Omega, Phi, Lambda)
    results = {}
    results["graph name"] = graph_name
    results["sols match"] = PAPER['solution'] == OUTPUTV2['objVal']
    results["og fail"] = PAPER['fail']
    results["v2 fail"] = OUTPUTV2['fail']
    results["v2 faster"] = OUTPUTV2['total time'] < PAPER['time']
    results["og time"] = PAPER['time']
    results["v2 time"] = OUTPUTV2['total time']
    results["time diff"] = results["v2 time"] - results["og time"]
    results["og obj"] = PAPER['solution']
    results["v2 obj"] = OUTPUTV2['objVal']
    results["og X"] = OUTPUTV2['X_sol']
    results["v2 X"] = PAPER['X_sol']
    results["og Y"] = OUTPUTV2['Y_sol']
    results["v2 Y"] = PAPER['Y_sol']
    results["og Z"] = OUTPUTV2['Z_sol']
    results["v2 Z"] = PAPER['Z_sol']
    #results["og last AD Tm"] = PAPER["last_AD_time"]
    return results


def run_MCN_all_nums(N, density, Budgets, timelimit=False):
    """
    Tests MCN against results from the paper for all 20 instances
    of the given parameters.
    """
    Data = []
    Timeouts = []
    if not timelimit:        
        for num in Numbers:
            print(f"\n--> TESTING GRAPH {num}")
            results = run_MCN_single(N, num, density, Budgets)
            Data.append(results)
    else: ## broken
        signal.signal(signal.SIGALRM, timeout_handler)
        for num in Numbers:
            print(f"\n--> TESTING GRAPH {num}")
            signal.alarm(timelimit)
            try:
                results = run_MCN_single(N, num, density, Budgets)
                Data.append(results)
            except Exception:
                continue
    graphname = get_filename2(N, density, Budgets)
    export_results(Data, graphname)
    return Data, Timeouts


def run_MCN_budgets(Budgets, timelimit=False):
    # tests against all rndgraph instances with the given budget
    TIMEOUTS = {}
    for N in Ns:
        for dens in Density:
            graph_name = get_filename2(N, dens, Budgets)
            path = f"./Instances/tables_MNC/{graph_name}"
            if os.path.exists(path):
                Data, timeouts = run_MCN_all_nums(N, dens, Budgets,timelimit=timelimit)
                TIMEOUTS[graph_name] = timeouts
    return TIMEOUTS


def get_v2_result(N, density, Budgets):
    """
    Returns most recently exported csv of graph structure
    as a dataframe
    """
    graph_name = get_filename2(N,density,Budgets)
    if graph_name not in os.listdir(RESULTS_PATH):
        raise Exception(f"No results for graph {graph_name}")
    else:
        path = RESULTS_PATH+graph_name+'/'
        file = os.listdir(RESULTS_PATH+graph_name+'/')[-1]
        data = pd.read_csv(path+file)
    return data
        

def count_matching_solutions():
    MATCHES = {}
    for graph in os.listdir(RESULTS_PATH):
        path = RESULTS_PATH+graph+'/'
        file = os.listdir(RESULTS_PATH+graph+'/')[-1]
        data = pd.read_csv(path+file)
        MATCHES[graph] = sum(int(result) for result in data['sols match'])
    MATCHES.to_csv(RESULTS_PATH+'sol_check-'+get_timestamp()+'.csv')
    return MATCHES

def timeout_handler(signum, frame):
    raise Exception


# ------------------------------------------------------------------------ #

def main():
    timeouts = run_MCN_budgets([1,1,1])
    matches = count_matching_solutions()

if __name__ == "__main__":
    main()
