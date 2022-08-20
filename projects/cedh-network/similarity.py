import json
import sys
import math
import random
from pyvis.network import Network
sys.path.insert(0, '../api')
import mtg_api



with open('ddb_decks_entry.json', 'r') as f:
    data = json.load(f)
count = 0
for selected_deck in data.keys():
    print(selected_deck, count)
    count += 1
    nodes = []
    selected_decklist = list(data[selected_deck]['deck']['mainboard'].keys())
    for name, info in data.items():
        deck = info['deck']
        color = info['colors']
        commander = list(deck['commanders'].keys())
        if name == selected_deck:
            distance = 0
        else:
            decklist = list(deck['mainboard'].keys())
            distance = len(set(decklist).symmetric_difference(set(selected_decklist)))
        nodes.append({'name': name, 'commander': commander, 'image': 'http://24.62.6.16/color/'+color+'.png', 'distance': distance})
    with open('deck_distances.json', 'w') as f:
        f.write(json.dumps(nodes, indent=4))

    html = """
    <html>
        <head>
        </head>
        <body>
        {body}
        </body>
    </html
    """
    body = ''

    with open('deck_distances.json', 'r') as f:
        nodes = json.load(f)

    for node in nodes:
        if  node['distance'] != 0:
            distance = node['distance']
        else:
            distance = 0
        angle = random.randint(1, 360)
        x = 50 + ((distance * math.sin(angle)))/3
        y = 50 + ((distance * math.cos(angle)))/3

        body += """
                <div style="position:absolute; left:{x}%; top:{y}%; transform: translate(-50%, -50%);">
                    <a href="/similar/{name_url}"><img src="{image}" style="width:30px;height:30px;"><br></a>
                    <span>{name}</span>
                </div>
                """.format(x=x, y=y, name_url=node['name'].replace(' ', '_').replace('/', ';'), image=node['image'], name=node['name'])
        with open('../../site/templates/similarities/'+selected_deck.replace(' ', '_').replace('/', ';')+'.html', 'w') as f:
            f.write(html.format(body=body))
