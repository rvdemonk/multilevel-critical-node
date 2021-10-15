from gurobipy import *
from assignment.project.Protect import Protect
from test_defend import nodes_, edges_


def rlxAP(Nodes, Edges, Phi, Lambda):
    A = Model("Attack")
    A.setParam("NonConvex", 2)
    # Variables
    y = {v: A.addVar(vtype=GRB.BINARY) for v in Nodes}
    h = {v: A.addVar(lb=0) for v in Nodes}
    q = {(u, v): A.addVar(lb=0) for (u, v) in Edges}
    p = A.addVar(lb=0)
    gamma = {v: A.addVar(lb=0) for v in Nodes}

    A.setObjective(Lambda * p + quicksum(gamma[v] for v in Nodes), GRB.MINIMIZE)

    # Constraints
    AttackBudget = A.addConstr(quicksum(y[v] for v in Nodes) <= Phi)
    Constr1 = {
        v: A.addConstr(
            h[v]
            + quicksum(q[u, v] for (u, v) in Edges)
            - quicksum(q[v, u] for (v, u) in Edges)
            >= 1
        )
        for v in Nodes
    }

    Constr2 = {
        v: A.addConstr(p - quicksum(q[u, v] for (u, v) in Edges) >= 0) for v in Nodes
    }

    Constr3 = {v: A.addConstr(gamma[v] + len(Nodes) * y[v] - h[v] >= 0) for v in Nodes}

    SignConstr_p = A.addConstr(p >= 0)
    for v in Nodes:
        A.addConstr(h[v] >= 0)
        A.addConstr(gamma[v] >= 0)

    for (u, v) in Edges:
        A.addConstr(q[u, v] >= 0)

    A.optimize()
    print("best infection: ", A.objVal)
    Infected = [int(round(y[v])) for v in Nodes]
    return A, Infected, A.objVal


def AP(Nodes, Edges, Phi, Lambda, target):
    best = len(Nodes)
    I_best = []
    status = 0
    while status != GRB.INFEASIBLE:
        AP_model, I, value = rlxAP(Nodes, Edges, Phi, Lambda)
        if value <= target - 1:
            return (I, "goal")
        Saved, Protected = Protect(Nodes, Edges, Infected=I_best, Lambda=Lambda)
        if len(Saved) <= target - 1:
            return (I, "goal")
        if len(Saved) < best:
            best = len(Saved)
            I_best = I
        # Add cut
        # Might have to restructure entire file to add this cut
    return (I_best, "opt")

APmodel = rlxAP(nodes_, edges_, 2, 2)
print(APmodel.status)
