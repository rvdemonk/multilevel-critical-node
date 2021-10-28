from gurobipy import *


def Defend(Nodes, Edges, Infected, Lambda):
    """
    Defence problem (fence problem)
    Infected: set of indices of nodes infected by given attack strategy.
    Lambda: Defence budget
    """
    # Create attack vector from set of infected nodes taken as input
    Y = {v: 1 if v in Infected else 0 for v in Nodes}

    D = Model("Defend")
    D.setParam("OutputFlag", 0)

    # Variables
    A = {v: D.addVar(vtype=GRB.BINARY) for v in Nodes}  # saved nodes
    X = {v: D.addVar(vtype=GRB.BINARY) for v in Nodes}  # defended nodes

    D.setObjective(quicksum(A[v] for v in Nodes), GRB.MAXIMIZE)

    # Constraints
    DefendBudget = D.addConstr(quicksum(X[v] for v in Nodes) <= Lambda)
    ViralSpread = {v: D.addConstr(A[v] <= 1 - Y[v]) for v in Nodes}
    SavedNodes = {(u, v): D.addConstr(A[v] <= A[u] + X[v]) for (u, v) in Edges}

    D.optimize()

    # Saved nodes
    Saved = set(v for v in Nodes if A[v].x > 0.9)
    # Defence strategy
    Defended = set(v for v in Nodes if X[v].x > 0.9)

    return Saved, Defended
