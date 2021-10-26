from gurobipy import *

from Defend import Defend



def AP(Nodes, Edges, Phi, Lambda, target):

    # (rlxAP)

    AP = Model("AttackDefend")
    AP.setParam("OutputFlag", 0)
    AP.setParam("NonConvex", 2)  # for McCormick evenelope


    # Variables

    y = {v: AP.addVar(vtype=GRB.BINARY) for v in Nodes}
    # y = {v: A.addVar() for v in Nodes} # complete relaxation still didnt solve
    h = {v: AP.addVar(lb=0) for v in Nodes}
    q = {(u, v): AP.addVar(lb=0) for (u, v) in Edges}
    p = AP.addVar(lb=0)
    gamma = {v: AP.addVar(lb=0) for v in Nodes}
    AP.setObjective(Lambda * p + quicksum(gamma[v] for v in Nodes), GRB.MINIMIZE)

    # Constraints
    AttackBudget = AP.addConstr(quicksum(y[v] for v in Nodes) <= Phi)
    Constr1 = {
        v: AP.addConstr(
            h[v]
            + quicksum(q[u, v] for (u, v) in Edges)
            - quicksum(q[v, u] for (v, u) in Edges)
            >= 1
        )
        for v in Nodes}

    Constr2 = {
        v: AP.addConstr(p - quicksum(q[u, v] for (u, v) in Edges) >= 0) for v in Nodes
    }

    Constr3 = {v: AP.addConstr(gamma[v] + len(Nodes) * y[v] - h[v] >= 0) for v in Nodes}


    ###### AP Subroutine ######
    best = len(Nodes)
    Infected_best = set()
    X_best = []
    status = 0
    CutsAdded = 0

    while True:
        AP.optimize()
        if AP.status == GRB.INFEASIBLE:
            break
        Infected = set(v for v in Nodes if y[v].x > 0.9)
        if AP.objVal <= target - 1:
            return (Infected, "goal", [])
        Saved, Defended = Defend(Nodes, Edges, Infected=Infected, Lambda=Lambda)
        if len(Saved) <= target - 1:
            return (Infected, "goal", Defended)
        if len(Saved) < best:
            best = len(Saved)
            Infected_best = Infected
            X_best = Defended
        # Add cut
        AP.addConstr(quicksum(y[v] for v in Saved) >= 1)
        CutsAdded += 1
        
    return Infected_best, "optimal", X_best
