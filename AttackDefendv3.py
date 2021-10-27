from gurobipy import *
from Defendv3 import Defend


def AP(Nodes, Arcs, Phi, Lambda):
    # Value function formulation
    AP = Model('Attack')
    A = {v: AP.addVar() for v in Nodes}
    Y = {v: AP.addVar() for v in Nodes}
    X = {v: AP.addVar() for v in Nodes}

    AP.setObjective(quicksum(A[v] for v in Nodes), GRB.MINIMIZE)

    # Constraints
    AttackBudget = AP.addConstr(quicksum(Y[v] for v in Nodes)<=Phi)

    # Follower constraints
    DefendBudget = AP.addConstr(quicksum(X[v] for v in Nodes)<=Lambda)

    # Attacked node constraints
    SavedNodes = {
        v: AP.addConstr(A[v]<= 1-Y[v])
        for v in Nodes
    }
    ViralSpread = {
        (u,v): AP.addConstr(A[v]<=A[u]+X[v])
    }

    # relax HPR by removing constr (13)
    # 
    # run Fischetti HPR algo
    BMP.setParam('LazyConstraints',1)
    AP.optimize(Callback)
    return


def Callback(model,where):
    if where==GRB.Callback.MIPNODE and model.cbGet(GRB.Callback.MIPNODE_STATUS)==GRB.OPTIMAL:
        # integer solution at current node
        YV = model.cbGetSolution(Y)
        YSet = {v for v in YV if YV[v]>0.9}
        XV = model.cbGetSolution(X)
        # Compute value function for Y by solving Defend for Y=Y*
        ValueFunc = Defend(Nodes,Arcs,Yset,Lambda)
        if dy <= ValueFunc:
            # current solution is bilevel feasible
            # update the incumbent and fathom the current node
            pass
        else:
            # if not all int y variables are fixed by branching

            # else


    return