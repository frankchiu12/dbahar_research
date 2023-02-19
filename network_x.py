import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('', nrows=100)

g = nx.Graph()

counter = 0
prev_id = None
for id in df['inventor_id']:
    if id not in df:
        g.add_node(id, weight=1)
    else:
        g.node[id]["weight"] += 1
    if counter > 1:
        g.add_edge(prev_id, id)
    prev_id = id
    counter += 1

nx.draw(g, with_labels = True)
plt.savefig('graph.png')