from unittest import TestCase
from DefendAttackDefend2 import MCN
from data import *
from test_mcn import *
from helpers import get_filename2


graph_base_name = "rndgraph"
Ns = [20, 40, 60, 80, 100]
BudgetSet = [[1, 1, 1], [3, 1, 3], [2, 2, 2], [3, 3, 1], [1, 3, 3], [3, 3, 3]]
Numbers = [f"00{i}" for i in range(1, 10)] + [f"0{j}" for j in range(10, 21)]
Density = range(5, 16)

# Budgets = [2,2,2]
# density = 5
# N = 40
# correct = 0
# for num in Numbers:
#     results = test_MCN_single(N,num,density,Budgets)
#     if results["sols match"]:
#         correct+=1


# print(f"\nResults for N={N}, density={density}, Budets={Budgets}")
# print(f"Matching sols: {correct} out of 20")


def test_solutions(TestBudgets):
    folder = "./Instances/tables_MNC/"
    MATCHING_SOLS = {}
    Unrecognised = []
    for N in Ns:
        for density in Density:
            for Budgets in TestBudgets:
                name = get_filename2(N, density, Budgets)
                folderpath = folder + name + "/"
                if not os.path.isdir(folderpath):
                    print(f"{folderpath} is is not a recognised graph structure")
                    Unrecognised.append(name)
                    break
                else:
                    MATCHING_SOLS[name] = 0
                    print("Testing", name)
                    for num in Numbers:
                        results = test_MCN_single(N, num, density, Budgets)
                        if results["sols match"]:
                            MATCHING_SOLS[name] += 1

    for key in MATCHING_SOLS:
        print(f"\n{key}")
        print("Matching solutions:", MATCHING_SOLS[key])
    return MATCHING_SOLS, Unrecognised
