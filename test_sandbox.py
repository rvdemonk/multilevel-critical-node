from test_mcn import export_results, test_MCN_all_nums, RESULTS_PATH
import pandas as pd
from helpers import get_graph_data, get_paper_stats, get_filename2
import os
from DefendAttackDefend import MCN
from AttackDefend import AP


test_case = "05-40_2-2-2"

Nodes, Arcs = get_graph_data('002',40,5,2,2,2)

# Y_opt_set, status, Defended = AP(Nodes, Arcs,2,2,26)

output, objVal, Prot_best, Y_best, Defend_best, Saved_best = \
    MCN(Nodes,Arcs,2,2,2)

print(f"Nodes saved: {objVal}.....{len(Saved_best)}")
print(f"Protected: {Prot_best}")
print(f"Attacked: {Y_best}")
print(f"Defended: {Defend_best}")
