from gurobipy import *
from Defendv3 import Defend


def AP(Nodes, Arcs, Phi, Lambda):
    # Value function formulation
    EPS = 0.0001
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


    def Callback(model,where):
        # Branching strategy
        if where==GRB.Callback.MIPNODE and model.cbGet(GRB.Callback.MIPNODE_STATUS)==GRB.OPTIMAL:
            # new integer solution found (x*,y*)
            YV = model.cbGetSolution(Y) #y*
            YSet = {v for v in YV if YV[v]>0.9}
            XV = model.cbGetSolution(X)
            # Is this incumbent solution bilevel feasible? -> solve Defend with y = y*
            SavedNodes, DefendedNodes = Defend(Nodes,Arcs,YSet,Lambda)
            Value = len(SavedNodes)
            if  model.cbGet(GRB.Callback.MIPNODE_OBJBST)+EPS >= Value:
                # solution is bilevel feasible
                pass
            else:
                # solution is not bilevel feasible
                pass
                

        return


    # relax HPR by removing constr (13)

    # run Fischetti HPR algo
    AP.setParam('LazyConstraints',1)
    AP.optimize(Callback)

    return