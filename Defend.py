from gurobipy import *


def Defend(Nodes, Edges, Infected, Lambda):
    """
    * Infected - binary vector; Infected_i = 1 if node i is infected, 0 otherwise.
    * Lambda - Defence budget
    """
    Y = {v : 1 if v in Infected else 0 for v in Nodes}

    D = Model("Defend")
    D.setParam('OutputFlag',0)
    
    # Variables
    A = {v: D.addVar(vtype=GRB.BINARY) for v in Nodes}  # saved nodes
    X = {v: D.addVar(vtype=GRB.BINARY) for v in Nodes}  # defended nodes

    D.setObjective(quicksum(A[v] for v in Nodes), GRB.MAXIMIZE)
    
    # Constraints
    DefendBudget = D.addConstr(quicksum(X[v] for v in Nodes) <= Lambda)
    ViralSpread = {v: D.addConstr(A[v] <= 1 - Y[v]) for v in Nodes}
    SavedNodes = {(u, v): D.addConstr(A[v] <= A[u] + X[v]) for (u, v) in Edges}

    D.optimize()

    # stats
    Saved = set(v for v in Nodes if A[v].x > 0.9)
    Defended = set(v for v in Nodes if X[v].x > 0.9)
    
    return Saved, Defended
