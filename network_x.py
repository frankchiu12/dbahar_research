import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('PatentsInventors.csv')

g = nx.Graph()

g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(1, 4)
g.add_edge(1, 5)

nx.draw(g, with_labels = True)
plt.savefig('graph.png')