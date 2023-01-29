from pyvis.network import Network
import os
import json
import sys
import copy
import numpy as np
import psycopg2
sys.path.insert(0, '../api')
import mtg_api

def generate_tierlist(min_count, decks, top16s, avg_attendents, images, name):
    decks = copy.deepcopy(decks)
    top16s = copy.deepcopy(top16s)
    avg_attendents = copy.deepcopy(avg_attendents)
    ratios = {}
    for commander in decks:
        if decks[commander] < min_count:
            del avg_attendents[commander]
            continue
        if commander not in top16s:
            ratios[commander] = 0
        else:
            ratios[commander] = top16s[commander]/decks[commander] * 100

    counts = {k: v for k, v in reversed(sorted(decks.items(), key=lambda item: item[1]))}
    ratios = {k: v for k, v in reversed(sorted(ratios.items(), key=lambda item: item[1]))} 
    tiers = {'100': [[]], '90': [[]], '80': [[]], '70': [[]], '60': [[]], '50': [[]], '40': [[]], '30': [[]], '20': [[]], '10': [[]], '0': [[]]}
    tiers_count = {'100': 0, '90': 0, '80': 0, '70': 0, '60': 0, '50': 0, '40': 0, '30': 0, '20': 0, '10': 0, '0': 0}

    for commander, ratio in ratios.items():
        for key in tiers:
            i = int(key)
            if ratio >= i and ratio < i + 9.99999999999999999999999999999999:
                if len(tiers[key][-1]) >= 10:
                    tiers[key].append([])
                tiers[key][-1].append((commander, ratio))
                tiers_count[key] += 1

    def chart(nodes, edges, file_name):
        net = Network(height='100%', width='100%')
        button = False
        if not button:
            net.set_options("""{
                "layout": {
                    "hierarchical": {
                        "direction": "UD",
                        "nodeSpacing": 10
                    }
                }
            }""")
        ranges = []
        level_count = 0
        for i in tiers:
            if i == '100':
                ranges.append('100% Turnover')
                net.add_node('100% Turnover', shape='circle', level=0)
            else:
                ranges.append(i+'-'+str(int(i)+9)+'% Turnover')
                net.add_node(i+'-'+str(int(i)+9)+'% Turnover', shape='circle', level=level_count)
            level_count += len(tiers[i])
        for num in ranges[1:]:
            net.add_edge(ranges[0], num, color='white')

        overunderplayed = {}
        max_size = 0
        for node in nodes:
            if node['size'] > max_size:
                max_size = node['size']
        for node in nodes:
            overunderplayed[node['commander']] = (max_size - node['size']) * ratios[node['commander']]
            
        
        overunderplayed = {k: v for k, v in reversed(sorted(overunderplayed.items(), key=lambda item: item[1]))}
        over_value = np.percentile(list(overunderplayed.values()),75)
        under_value = np.percentile(list(overunderplayed.values()), 25)

        for node in nodes:
            if node['size'] == 0:
                node['size'] = .5
            node['size'] = node['size'] / max_size * 100 
            if overunderplayed[node['commander']] > over_value:
                color = 'green'
                w = 5
            elif overunderplayed[node['commander']] < under_value:
                color = 'red'
                w = 5
            else:
                color = 'black'
                w = 1
            net.add_node(node['commander'], label=node['commander'].replace(';', '\n'), color=color, borderWidth=w, size=node['size'], title='Played '+str(round(counts[node['commander']], 2))+' times\n'+str(round(ratios[node['commander']],2))+'% Conversion Rate\n'+str(round(node['attendents'], 2))+' Average Attendents', shape='circularImage', level=node['tier'], image=node['image'])
        for edge in edges:
            net.add_edge(edge['source'], edge['dest'], color='white')
        if button:
            net.show_buttons(filter_=['layout'])
        net.save_graph(file_name) 

    nodes = []
    edges = []
    i = 0
    for tier in tiers:
        for l in tiers[tier]:
            for (key, value) in l:
                nodes.append({'commander': key, 'attendents':avg_attendents[key], 'size': counts[key], 'tier': i, 'image': images[key]})
            i += 1

    max_tier_length = 0
    for tier in tiers:
        for l in tiers[tier]:
            if len(l) > max_tier_length:
                max_tier_length = len(l)

    for i in range(max_tier_length):
        for tier in tiers:
            for l in tiers[tier]:
                for tier2 in tiers:
                    for l2 in tiers[tier2]:
                        if l != l2:
                            try:
                                edges.append({'source': l[i][0], 'dest': l2[i][0]})
                            except:
                                pass

    chart(nodes, edges, '../../site/templates/graphs/'+name)

decks = {}
top16s = {}
avg_attendents = {}
images = {}

conn = psycopg2.connect("dbname='cedh' user='pi' host='localhost' password='password'")
cur = conn.cursor()
cur.execute('SELECT * from tiers;')
data = cur.fetchall()
for row in data:
    decks[row[1]] = row[2]
    top16s[row[1]] = row[3]
    avg_attendents[row[1]] = row[4]
    images[row[1]] = row[5]



play_counts = set(list(decks.values()))
print(play_counts)
for i in play_counts:
    print('    ', i)
    generate_tierlist(i, decks, top16s, avg_attendents, images, 'graph_'+str(i)+'.html')