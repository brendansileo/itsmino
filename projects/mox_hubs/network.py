from pyvis.network import Network
import matplotlib.pyplot as plt
import random
import json
import sys
import networkx as nx
import numpy as np
from PIL import Image
sys.path.insert(0, '../api')
import mtg_api

def random_color():
    r = lambda: random.randint(100,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def chart(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)
    #pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())))
    plt.figure(3,figsize=(32,32)) 
    nx.draw_kamada_kawai(G, node_size=500, with_labels='True', node_color='green', font_size=12, font_weight='bold')
    plt.savefig("Graph.jpg", format="JPEG")
    foo = Image.open('Graph.jpg')
    foo.save('Graph.jpg', optimize=True, quality=95)

with open('hub_counts.json', 'r') as f:
    data = json.load(f)
nodes = []
edges = []
for hub, connections in data.items():
    nodes.append(hub)
    for connection, weight in connections.items():
        edges.append([hub, connection, weight])
chart(nodes, edges)
