from gurobipy import *
from AttackDefend import AP
import time


def MCN(Nodes, Edges, Omega, Phi, Lambda):
    startTime = time.time()
    MAX_ITER = 50
    output = {}

    DAP = Model("DefendAttackDefend")
    DAP.setParam('OutputFlag',0)

    # global variables
    Z = {v: DAP.addVar(vtype=GRB.BINARY) for v in Nodes} # vaccinated
    delta = DAP.addVar()
    DAP.setObjective(delta, GRB.MAXIMIZE)
    # budget constraint
    VaccBudget = DAP.addConstr(quicksum(Z[v] for v in Nodes)<=Omega)

    ### MCN routine ###
    N = len(Nodes)
    D = [] # set of vaccinated nodes
    Q = [] # list of sets of attacked nodes
    best = len(Nodes) # start with all nodes saved
    A_y = []
    X_y = []
    cnt = 0
    
    while True:
        print(f"...Beginning iteration {cnt}")
        if cnt > MAX_ITER:
            output["fail"] = True
            return output
        # removed vaxxed nodes from attacker target
        target = best - len(D)
        #Nodes_D = set(Nodes) - D
        Nodes_D = [v for v in Nodes if v not in D]
        Edges_D = [edge for edge in Edges if edge[0] not in D and edge[1] not in D]
        Y_opt, status, Protected = AP(Nodes_D, Edges_D, Phi, Lambda, target)
        Y_opt_vector = [1 if v in Y_opt else 0 for v in Nodes]
        if status == "optimal":
            # there is no attack that results in less nodes saved
            endTime = time.time()
            output["total_time"] = round(endTime-startTime, 3)
            output["fail"] = False
            output["opt_sol"] = int(best)
            output["opt_vac"] = D
            output["opt_attack"] = Y_opt
            output["opt_protect"] = Protected
            output["num_iterations"] = cnt
            return output

        elif status == "goal":
            # there exists an attack that results in less than target
            # nodes saved, ie a better attack, then add the attack
            # vector to Q
            Q.append(Y_opt) # add new optimal attack to attack scenarios
            # 1lvMip_Q variables corresponding to Y_opt_incumbent
            X_y.append(
                {v: DAP.addVar(vtype=GRB.BINARY) for v in Nodes}
            )
            A_y.append(
                {v: DAP.addVar(lb=0, ub=1) for v in Nodes}
            )
            # constraints corresponding to attack scenario y_opt_incumbent
            # constraint names correspond to order presented in 1lvMIP model
            Constr1 = DAP.addConstr(delta <= quicksum(A_y[cnt][v] for v in Nodes)) 

            Constr3 = DAP.addConstr(quicksum(X_y[cnt][v] for v in Nodes) <= Lambda)  

            ### problem: key error with Y_opt, shortens to not incude vaxxed nodes

            Constr4 = [DAP.addConstr(
                    A_y[cnt][v] <= 1 + Z[v] - Y_opt_vector[v-1]
                    ) 
                    for v in Nodes]

            Constr5 = [DAP.addConstr(
                    A_y[cnt][v] <= A_y[cnt][u] + X_y[cnt][v] + Z[v]
                    )
                    for (u,v) in Edges]
            
            # solve model -> (D, best)
            DAP.optimize()
            D = [v for v in Nodes if Z[v].x > 0.9]
            best = DAP.objVal    
            cnt += 1
    ## ----------------------------------------------------------------- ##

