from gurobipy import *
from Defendv3 import Defend
from helpers import get_high_traffic_nodes


def AP(Nodes, Arcs, Phi, Lambda, target):
    # Value function formulation
    EPS = 0.0001
    AP = Model('Attack')
    A = {v: AP.addVar(vtype=GRB.BINARY) for v in Nodes}
    Y = {v: AP.addVar(vtype=GRB.BINARY) for v in Nodes}
    X = {v: AP.addVar(vtype=GRB.BINARY) for v in Nodes}

    AP.setObjective(quicksum(A[v] for v in Nodes), GRB.MINIMIZE)

    # Constraints
    AttackBudget = AP.addConstr(quicksum(Y[v] for v in Nodes) == Phi)

    # Follower constraints
    DefendBudget = AP.addConstr(quicksum(X[v] for v in Nodes) == Lambda)

    # Attacked node constraints
    SavedNodes = {
        v: AP.addConstr(A[v]<= 1-Y[v])
        for v in Nodes
    }
    ViralSpread = {
        (u,v): AP.addConstr(A[v]<=A[u]+X[v])
        for (u,v) in Arcs
    }
    
    MAX_NODE_CUTS = 5
    _callbackCount = {}
    def Callback(model,where):
        if where==GRB.Callback.MIPSOL:
            currentNode = model.cbGet(GRB.Callback.MIPNODE_NODCNT)
            print(f"### At node {currentNode}")
            if currentNode in _callbackCount:
                _callbackCount[currentNode] += 1
            else:
                _callbackCount[currentNode] = 1
                critNodes = get_high_traffic_nodes(Nodes,Arcs,Phi) # worst outcome for defense
                SavedNodes, DefendedNodes = Defend(Nodes,Arcs,critNodes,Lambda)
                FUB = len(SavedNodes)
                # for v in Nodes:
                #     if v in DefendedNodes:
                #         model.addConstr(X[v]==1)
                #     else:
                #         model.addConstr(X[v]==1)
                model.cbLazy(quicksum(A[v] for v in Nodes) >= FUB)

            # ICs - for every callback, with a max number of calls
            if _callbackCount[currentNode] < MAX_NODE_CUTS:
                pass

        # # Branching strategy
        # if where==GRB.Callback.MIPNODE and model.cbGet(GRB.Callback.MIPNODE_STATUS)==GRB.OPTIMAL:
        #     # new integer solution found (x*,y*)
        #     YV = model.cbGetSolution(Y) #y*
        #     YSet = {v for v in YV if YV[v]>0.9}
        #     XV = model.cbGetSolution(X)
        #     # Is this incumbent solution bilevel feasible? -> solve Defend with y = y*
        #     SavedNodes, DefendedNodes = Defend(Nodes,Arcs,YSet,Lambda)
        #     VF = len(SavedNodes)
        #     if  model.cbGet(GRB.Callback.MIPNODE_OBJBST)+EPS >= VF:
        #         # UPDATE INCUMBENT
        #         # fathom the node
        #         pass
        #     else:
        #         # if not all x_j variables with j in J_f are fixed by branching

        #         # else
        #         model.addConstr(quicksum(A[v] for v in Nodes) <= VF)
        #         if  model.cbGet(GRB.Callback.MIPNODE_OBJBST)+EPS >= VF:
        #             # update solution
                    # pass


    # relax HPR by removing constr (13)

    # run Fischetti HPR algo
    AP.setParam('LazyConstraints',1)
    AP.setParam('Presolve',0)
    AP.optimize(Callback)

    YSet = {v for v in Y if Y[v].x>0.9}
    status = 'optimal'
    XSet = {v for v in X if X[v].x>0.9}
    print(AP.objVal)
    print([Y[v].x for v in Nodes])
    return YSet, status, XSet