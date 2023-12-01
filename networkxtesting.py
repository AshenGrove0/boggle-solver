import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Object():
    def __init__(self, value):
        self.value = value

o1 = Object(12)

graph = nx.MultiDiGraph()

edge_list = [(1,2),(2,3),(4,1),(3,1),(2,5), (5,1), (5,6)]
'''
g = nx.from_numpy_array(np.array([[0,1,0],
          [1,1,1],
          [0,0,0]]))'''

#g = nx.complete_graph(5)


g = nx.Graph()


g.add_edges_from(edge_list)
print(dict(g.degree))
#print(nx.adjacency_matrix(g))
nx.draw_spring(g, with_labels=True)
#nx.draw_shell(g, with_labels=True)

plt.show()

'''g = nx.Graph()

g.add_edge(1,2)
g.add_edge(2,3, weight=0.9)

g.add_edge("A","B")
g.add_edge("B","c", weight=0.2)
g.add_node("D")
g.add_edge("D",1)
g.add_edge("D","A")
g.add_node(o1)
g = nx.Graph()

nx.draw_spring(g, with_labels=True)

plt.show()
'''
