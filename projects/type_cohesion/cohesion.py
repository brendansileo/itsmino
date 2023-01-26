import json
import requests

#r = requests.get('https://api.scryfall.com/catalog/creature-types').json()
#types = r['data']
#
#def get_types(url):
#    r = requests.get(url).json()
#    if 'status' in r:
#        return
#    for creature in r['data']:
#        print('    '+creature['name'])
#    if r['has_more']:
#        get_types(r['next_page'])
#
#for type in types:
#    print(type)
#    get_types('https://api.scryfall.com/cards/search?q=t%3Acreature+t%3A'+type)

with open('tags.txt', 'r') as f:
    data = f.read()

tags = []

data = data.split('\n\n')
for d in data:
    if '(functional)' in d:
        d = d.split('\n')[1]
        t = d.split(' · ')
        tags.extend(t)

creatures_by_tag = {}

def get_creatures(tag, url):
    print(tag)
    creatures_by_tag[tag] = []
    r = requests.get(url).json()
    if 'data' not in r:
        return
    for card in r['data']:
        if card['name'] not in creatures_by_tag[tag]:
            creatures_by_tag[tag].append(card['name'])
    if r['has_more']:
        get_creatures(tag, r['next_page'])

for tag in tags:
    get_creatures(tag, 'https://api.scryfall.com/cards/search?q=t%3Acreature+oracletag%3A'+tag)

with open('tags.json', 'w') as f:
    f.write(json.dumps(creatures_by_tag, indent=4))