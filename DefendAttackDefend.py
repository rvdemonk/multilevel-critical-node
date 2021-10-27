"""
@lewisthompson
"""
from gurobipy import *
from AttackDefend import AP
import time


def MCN(Nodes, Edges, Omega, Phi, Lambda):
    startTime = time.time()
    MAX_ITERATIONS = 50

    DAP = Model("ProtectAttackDefend")
    DAP.setParam("OutputFlag", 0)

    # Global variables
    Z = {v: DAP.addVar(vtype=GRB.BINARY) for v in Nodes}
    delta = DAP.addVar()

    DAP.setObjective(delta, GRB.MAXIMIZE)

    ProtBudget = DAP.addConstr(quicksum(Z[v] for v in Nodes) <= Omega)

    # --- MCN routine ---#
    count = 0
    OUTPUT = {}
    best_saved = len(Nodes)  # start with every node saved
    Protected = set()
    Q = []  # stores attack vectors
    X_y = []
    A_y = []
    while True:
        print(f"iteration {count}...")
        if count > MAX_ITERATIONS:
            OUTPUT["fail"] = True
            return OUTPUT

        attack_target = best_saved - len(Protected)
        Nodes_reduced = [v for v in Nodes if v not in Protected]
        Edges_reduced = [
            e for e in Edges if e[0] not in Protected and e[1] not in Protected
        ]

        # Find an attack against unprotected nodes that results in less
        # than attack_target nodes saved
        Attack_incumb, status, Defend_incumb = AP(
            Nodes_reduced, Edges_reduced, Phi, Lambda, attack_target
        )

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

            # Solve model for Protected nodes and objVal
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
            OUTPUT["iterations"] = count
            OUTPUT["saved nodes"] = [v for v in Nodes if A_y[-1][v].x > 0.9]

            VAR_COUNT = {}
            # VAR_COUNT['A_count'] =
            return OUTPUT

        else:
            print("!!! Error has occurred !!!")
    # ------------------------------------------------------------------------#
