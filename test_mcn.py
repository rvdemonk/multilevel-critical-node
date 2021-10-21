from pandas.core.indexing import need_slice
from DefendAttackDefend import MCN
from helpers import get_graph_data, get_paper_stats, get_filename, get_filename2
from data import graph_base_name, Ns, Density, BudgetSet, Numbers
import pandas as pd
from datetime import datetime
import os


RESULTS_PATH = "./results1"

def export_results(Results, graph_name):
    """
    Exports csv indexed by the number of the graph instance, 1-20
    """
    data = pd.DataFrame(Results, index=Numbers)
    timestamp = str(datetime.now()).replace(" ", "_").split(".")[0]
    timestamp = timestamp.replace("/","-").replace(":","-")
    path=RESULTS_PATH+f"/{graph_name}/"
    if not os.path.exists(path):
        os.mkdir(path)
    data.to_csv(os.path.join(path,rf"{graph_name}_@{timestamp}.csv"))
    print("*"*65+f"\nTesting of {graph_name}complete.\n"+"*"*65)


def test_MCN_single(N, number, density, Budgets):
    Omega, Phi, Lambda = Budgets[0], Budgets[1], Budgets[2]
    graph_name = get_filename(N, density, Omega, Phi, Lambda)
    nodes, edges = get_graph_data(number, N, density, Omega, Phi, Lambda)
    og_sol = get_paper_stats(number, N, density, Omega, Phi, Lambda)
    print(f"Testing {graph_name}_{number}")
    my_sol = MCN(nodes, edges, Omega, Phi, Lambda) 

    results = {}
    results['graph name'] = graph_name
    results['og fail'] = 0
    results['v2 fail'] = 0
    results['answers match'] = 0
    results['v2 faster'] = 0
    results['og time'] = 0
    results['v2 time'] = 0
    results['time diff'] = results['v2 time'] - results['og time']
    results['og obj'] = 0
    results['v2 obj'] = 0
    results['og X'] = 0
    results['v2 X'] = 0
    results['og Y'] = 0
    results['v2 Y'] = 0
    results['og Z'] = 0
    results['v2 Z'] = 0
    results['og last ']


    return


def test_MCN_all_nums(N, density, Budgets):
    """
    Tests MCN against results from the paper for all 20 instances
    of the given parameters.
    """
    Data = []
    for num in Numbers:
        print(f"\n--> TESTING GRAPH {num}")
        results = test_MCN_single(N, num, density, Budgets)
        Data.append(results)
    graphname = get_filename2(N, density, Budgets)
    export_results(Data, graphname)
    return Data
   

def test_MCN_budgets(Budgets):
    # tests against all rndgraph instances with the given budget
    for N in Ns:
        for dens in Density:
            graph_name = get_filename2(N, dens, Budgets)
            path=f"./Instances/tables_MNC/{graph_name}"
            if os.path.exists(path):
                Data = test_MCN_all_nums(N,dens,Budgets)
                export_results(Data, graph_name)
    return
    


# ------------------------------------------------------------------------ #

def main():
    #test_MCN_budgets([2,2,2])
    
    test_MCN_all_nums(40,5,[2,2,2])



if __name__ == "__main__":
    main()
    









        
