"""
@lewisthompson
MCNv2 implemented based on MCN from Baggio et al paper
Implemented for math4202 project.
"""
from gurobipy import *
from AttackDefend import AP
import time
from timeout_custom import timeout

TIMEOUT = 10 * 60


@timeout(TIMEOUT)
def MCNv2(Nodes, Edges, Omega, Phi, Lambda):
    startTime = time.time()
    MAX_ITERATIONS = 50

    DAP = Model("ProtectAttackDefend")
    DAP.setParam("OutputFlag", 0)

    # Global variables
    Z = {v: DAP.addVar(vtype=GRB.BINARY) for v in Nodes}
    delta = DAP.addVar()

    DAP.setObjective(delta, GRB.MAXIMIZE)

    # protection budget
    ProtBudget = DAP.addConstr(quicksum(Z[v] for v in Nodes) <= Omega)

    # --- MCNv2 routine ---#
    count = 0  # iteration count
    OUTPUT = {}  # store output stats
    best_saved = len(Nodes)  # start with every node saved
    Protected = set()  # protection strategy
    # store attack vectors as theyre generated
    Q = []
    # store variables corresponding to each attack scenario
    X_y = []
    A_y = []
    # data structs to keep stats on AP calls
    AP_iterations = []
    AP_cuts_added = []

    while True:
        print(f"iteration {count}...")
        if count > MAX_ITERATIONS:
            OUTPUT["fail"] = True
            return OUTPUT

        attack_target = best_saved - len(Protected)
        # compute new network topology following node vaccination
        Nodes_reduced = [v for v in Nodes if v not in Protected]
        Edges_reduced = [
            e for e in Edges if e[0] not in Protected and e[1] not in Protected
        ]

        # Find an attack against unprotected nodes that results in less
        # than attack_target nodes saved
        Attack_incumb, status, Defend_incumb, AP_iter_count, CutsAdded = AP(
            Nodes_reduced, Edges_reduced, Phi, Lambda, attack_target
        )
        AP_iterations.append(AP_iter_count)
        AP_cuts_added.append(CutsAdded)

        if "goal" in status:
            # Attack found that cripples more nodes
            # add attack to Q
            Q.append(Attack_incumb)
            Y = {v: 1 if v in Attack_incumb else 0 for v in Nodes}
            X_y.append({v: DAP.addVar(vtype=GRB.BINARY) for v in Y})
            A_y.append({v: DAP.addVar(vtype=GRB.BINARY) for v in Y})

            DeltaConstr = DAP.addConstr(delta <= quicksum(A_y[-1][v] for v in Nodes))

            DefBudget = DAP.addConstr(quicksum(X_y[-1][v] for v in Nodes) <= Lambda)

            SavedNodes = [DAP.addConstr(A_y[-1][v] <= 1 + Z[v] - Y[v]) for v in Nodes]

            ViralSpread = [
                DAP.addConstr(A_y[-1][j] <= A_y[-1][i] + X_y[-1][j] + Z[j])
                for (i, j) in Edges
            ]

            # Solve model for new protection strategy and objVal
            DAP.optimize()
            Protected = set(v for v in Nodes if Z[v].x > 0.9)
            best_saved = DAP.objVal
            count += 1

        elif "optimal" in status:
            # the optimal attack has been found and vaccinated against
            OUTPUT["total time"] = round(time.time() - startTime, 2)
            OUTPUT["fail"] = False
            OUTPUT["objVal"] = DAP.objVal
            OUTPUT["Z_sol"] = Protected
            OUTPUT["Y_sol"] = Attack_incumb
            OUTPUT["X_sol"] = Defend_incumb
            OUTPUT["saved nodes"] = [v for v in Nodes if A_y[-1][v].x > 0.9]
            OUTPUT["iterations"] = count
            OUTPUT["AP iterations"] = AP_iterations
            OUTPUT["AP cuts added"] = AP_cuts_added
            OUTPUT["Q size"] = len(Q)
            OUTPUT["Var count"] = DAP.NumVars
            OUTPUT["Constr count"] = DAP.NumConstrs
            return OUTPUT

        else:
            # something has gone seriously wrong
            print("!!! Error has occurred !!!")
    # ------------------------------------------------------------------------#
