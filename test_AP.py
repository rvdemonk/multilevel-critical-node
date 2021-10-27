from helpers import *
from AttackDefendv3 import *

Nodes, Edges = get_graph_data('001',20,5,3,3,3)

YSet, status, XSet = AP(Nodes, Edges, 3,3,-1)

print(YSet,XSet)