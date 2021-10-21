"""
@lewisthompson
Attempt at improving MCN algorithm
 - additional cut added: 
"""
from gurobipy import *
from AttackDefend import AP
import time

def MCN(Nodes, Edges, Omega, Phi, Lambda):
    startTime = time.time()
    MAX_ITERATIONS = 50

    DAP = Model("ProtectAttackDefend")
    DAP.setParam('OutputFlag',0)

    # Global variables
    Z = {v: DAP.addVar(vtype=GRB.BINARY) for v in Nodes}
    delta = DAP.addVar()

    DAP.setObjective(delta, GRB.MAXIMIZE)

    ProtBudget = DAP.addConstr(quicksum(Z[v] for v in Nodes)<=Omega)

    #--- MCN routine ---#
    count = 0
    OUTPUT = {} 
    best_saved = len(Nodes) # start with every node saved
    Protected = set()
    Q = [] # stores attack vectors
    X_y = []
    A_y = []
    while True:
        print(f"iteration {count}...")
        if count > MAX_ITERATIONS:
            OUTPUT['fail'] = True
            return OUTPUT

        attack_target = best_saved - len(Protected)
        Nodes_reduced = [v for v in Nodes if v not in Protected]
        Edges_reduced = [e for e in Edges if e[0] not in Protected and e[1] not in Protected]
        
        # Find an attack against unprotected nodes that results in less 
        # than attack_target nodes saved
        Attack_incumb, status, Defend_incumb = \
            AP(Nodes_reduced, Edges_reduced, Phi, Lambda, attack_target)

        if "goal" in status:
            # attack found that cripples more nodes
            # add attack to Q
            Q.append(Attack_incumb)
            Y = [1 if v in Attack_incumb else 0 for v in Nodes]
            X_y.append({v: DAP.addVar(vtype=GRB.BINARY) for v in Nodes})
            A_y.append({v: DAP.addVar(vtype=GRB.BINARY) for v in Nodes})

            c1 = DAP.addConstr(delta <= quicksum(A_y[count][v] for v in Nodes))
            c3 = DAP.addConstr(quicksum(X_y[count][v] for v in Nodes) <= Lambda)
            c4 = [DAP.addConstr(A_y[count][v]<=1+Z[v]-Y[v]) for v in Nodes] 
            c5 = [DAP.addConstr(A_y[count][j]<=A_y[count][i]+X_y[count][j]+Z[j]) for (i,j) in Edges]

            # Solve model for Protected nodes and objVal
            DAP.optimize()
            Protected = set(v for v in Nodes if Z[v].x>0.9)
            best_saved = DAP.objVal
            count+=1

        elif "optimal" in status:
            # the optimal attack has been found and vaccinated against
            OUTPUT['total time'] = time.time() - startTime
            OUTPUT['fail'] = False
            OUTPUT['objVal'] = DAP.objVal
            OUTPUT['Z opt'] = Protected
            OUTPUT['Y opt'] = Attack_incumb
            OUTPUT['X opt'] = Defend_incumb
            OUTPUT['iterations'] = count
            return OUTPUT

        else:
            print("!!! Error has occurred !!!")
    #------------------------------------------------------------------------#