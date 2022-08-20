from pyvis.network import Network
import matplotlib.pyplot as plt
import random
import json
import sys
import networkx as nx
sys.path.insert(0, '../api')
import mtg_api

def random_color():
    r = lambda: random.randint(100,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def chart(nodes, edges, file_name):
    net = Network(height='100%', width='100%')
    net.set_options("""
        options = {
            "edges": {
                "selfReferenceSize": null,
                "selfReference": {
                "angle": 0.7853981633974483
                },
                "smooth": {
                "forceDirection": "none"
                }
            },
            "physics": {
                "barnesHut": {
                "springLength": 250,
                "avoidOverlap": 0.6
                },
                "minVelocity": 0.11
            }
        }
        """)
    
    for node in nodes:
        size = 0
        for edge in edges:
            if node['name'] == edge['to'] or node['name'] == edge['from']:
                size += 1
        l = node['name']
        net.add_node(node['name'], label=l, size=20, shape='circularImage', image=node['image'], title=';'.join(node['commander']))
    for edge in edges:
        #with width
        #net.add_edge(edge['to'], edge['from'], value=edge['width'], label='', title=str(edge['label'])+' card difference', color='black')
        #without width
        net.add_edge(edge['to'], edge['from'], label='', title=str(edge['label'])+' card difference', color='black')
    net.save_graph(file_name)

with open('ddb_decks_entry.json', 'r') as f:
    data = json.load(f)
nodes = []
for name, info in data.items():
    commander = list(info['commanders'].keys())
    colors = []
    for c in commander:
        card = mtg_api.get_card(c)
        colors += card['color_identity']
    colors = list(set(colors))
    colors.sort()
    color = ''.join(colors).lower()
    nodes.append({'name': name, 'commander': commander, 'image': 'http://24.62.6.16/'+color+'.png'})
edges = []
max_distance = 30
for deck, deck_data in data.items():
    distances = {}
    for deck2, deck_data2 in data.items():
        deck_cards = list(deck_data['mainboard'].keys())
        deck2_cards = list(deck_data2['mainboard'].keys())
        distance = len(set(deck_cards).symmetric_difference(set(deck2_cards)))
        if distance > 0: #and distance < max_distance:
            edge = [deck, deck2]
            edge.sort()
            e_str = ';'.join(edge)
            if e_str not in distances:
                distances[e_str] = distance
    distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
    for i in list(distances.keys())[:3]:
        edge = i.split(';')
        distance = distances[i]
        edges.append({'to':edge[0], 'from':edge[1], 'width': max_distance-distance, 'label': distance})
chart(nodes, edges, '../../site/templates/graph2.html')
