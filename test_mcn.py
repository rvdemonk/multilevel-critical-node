from pandas.core.indexing import need_slice
from DefendAttackDefend import MCN
from helpers import get_graph_data, get_paper_stats, get_filename, get_filename2
from data import graph_base_name, Ns, Density, BudgetSet, Numbers
import pandas as pd
from datetime import datetime
import os


RESULTS_PATH = "./results"

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
    """
    Tests the MCN against the results of the original paper.
    """
    Omega, Phi, Lambda = Budgets[0], Budgets[1], Budgets[2]
    graph_name = get_filename(N, density, Omega, Phi, Lambda)
    nodes, edges = get_graph_data(number, N, density, Omega, Phi, Lambda)
    paper_solution = get_paper_stats(number, N, density, Omega, Phi, Lambda)
    
    print(f"Testing {graph_name}")
    my_solution = MCN(nodes, edges, Omega, Phi, Lambda)

    if my_solution["fail"] or 'no' in paper_solution["fail"]:
        results = {
        "graph_name": graph_name+f"_{number}",
        "imp_failed": my_solution["fail"] == True,
        "paper_fail": paper_solution["fail"],
        }
    else:
        results = {
            "graph_name": graph_name+f"_{number}",
            "imp_failed": my_solution["fail"] == True,
            "paper_fail": paper_solution["fail"],
            "answers_match": "yes" if my_solution["opt_sol"] == paper_solution["solution"] else "NO",
            "Z_sols_match": my_solution["opt_vac"] == paper_solution["Z_sol"],
            "improved_time": my_solution["total_time"] < paper_solution["time"],
            "imp_time": my_solution["total_time"],
            "paper_time": paper_solution["time"],
            "time_difference": round(my_solution["total_time"] - paper_solution["time"], 3),
            "imp_obj": my_solution["opt_sol"],
            "paper_obj": paper_solution["solution"],  
            "imp_X_sol": my_solution["opt_protect"],
            "paper_X_sol": paper_solution["X_sol"],
            "imp_Y_sol": my_solution["opt_attack"],
            "paper_Y_sol": paper_solution["Y_sol"],
            "imp_Z_sol": my_solution["opt_vac"],
            "paper_Z_sol": paper_solution["Z_sol"]
            }   
    return results


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
    
    test_MCN_all_nums(20,5,[2,2,2])



if __name__ == "__main__":
    main()
    









        
