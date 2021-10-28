""" 
Data stub for the MCN algorithm package.
Outlines parameters of randomgraph instances that are the
subject of experiments.
"""

TABLES = ["MNC", "MIX", "HIB"]
folder = "./Instances/tables_MNC/"

graph_base_name = "rndgraph"
Ns = [20, 40, 60, 80, 100]
BudgetSet = [[1, 1, 1], [3, 1, 3], [2, 2, 2], [3, 3, 1], [1, 3, 3], [3, 3, 3]]
Numbers = [f"00{i}" for i in range(1, 10)] + [f"0{j}" for j in range(10, 21)]
Density = range(5, 16)
