import json
import requests
import sys

mode = sys.argv[1]

if mode == 'load':
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

    with open('tags_without.json', 'w') as f:
        json.dump(creatures_by_tag, f, indent=4)

if mode == 'get_tagless':
    with open('tags_without.json', 'r') as f:
        tags = json.load(f)

    def get_creatures(creatures, url):
        r = requests.get(url).json()
        if 'data' not in r:
            return creatures
        for card in r['data']:
            if card['name'] not in creatures:
                creatures.append(card['name'])
        if r['has_more']:
            creatures = get_creatures(creatures, r['next_page'])
        return creatures

    creatures = []
    creatures = get_creatures(creatures, 'https://api.scryfall.com/cards/search?q=t%3Acreature')
    for tag, cs in tags.items():
        for c in cs:
            if c in creatures:
                creatures.remove(c)

    tags['untagged'] = creatures                
    with open('tags.json', 'w') as f:
        json.dump(tags, f, indent=4)

if mode == 'types':
    with open('tags.json', 'r') as f:
        tags = json.load(f)

    def get_types(creature):
        try:
            r = requests.get('https://api.scryfall.com/cards/named?exact='+creature.replace(' ','+')).json()
            types = r['type_line'].split(' — ')[1].split(' ')
        except:
            types = []
        return types

    done_creatures = []
    creature_types = {}
    types = {}
    for tag, creatures in tags.items():
        print(tag)
        for creature in creatures:
            creature_types[creature] = get_types(creature)
    with open('types.json', 'w') as f:
        json.dump(creature_types, f, indent=4)

if mode == 'raw':
    raw_cohesion = {}

    with open('tags.json', 'r') as f:
        tags = json.load(f)
    with open('types.json', 'r') as f:
        creatures = json.load(f)
    creatures = {k: v for k, v in sorted(creatures.items(), key=lambda item: item[0])}
    for creature, types in creatures.items():
        print(creature)
        for type in types:
            if type not in raw_cohesion:
                raw_cohesion[type] = {'count': 0, 'tags': {}}
            raw_cohesion[type]['count'] += 1
            for tag, cs in tags.items():
                if 'cycle' in tag or 'tribal' in tag or type.lower() in tag:
                    continue
                if creature in cs:
                    if tag not in raw_cohesion[type]['tags']:
                        raw_cohesion[type]['tags'][tag] = 0
                    raw_cohesion[type]['tags'][tag] += 1
            if raw_cohesion[type]['tags'] == {}:
                raw_cohesion[type]['tags']['no-tags'] = 0
            raw_cohesion[type]['tags'] = {k: v for k, v in reversed(sorted(raw_cohesion[type]['tags'].items(), key=lambda item: item[1]))}    
    with open('raw_cohesion.json', 'w') as f:
        json.dump(raw_cohesion, f, indent=4)

if mode == 'analyze':
    with open('raw_cohesion.json', 'r') as f:
        raw_cohesion = json.load(f)
    new_types = {}
    for type, info in raw_cohesion.items():
        new_types[type] = {'count': info['count'], 'tags': {}}
        for tag , count in info['tags'].items():
            if tag == 'untagged':
                continue
            print(type, tag)
            new_types[type]['tags'][tag] = count/info['count'] * 100

    def find_highest_value(new_types):
        highest = 0
        highest_type = None
        for type, info in new_types.items():
            if list(info['tags'].values())[0] >= highest:
                highest = list(info['tags'].values())[0]
                highest_type = type
        return highest_type

    sorted_types = {}
    x = len(new_types)
    while len(sorted_types) < x:
        k = find_highest_value(new_types)
        sorted_types[k] = new_types[k]
        del new_types[k]

    with open('cohesion.json', 'w') as f:
        json.dump(sorted_types, f, indent=4)

if mode == 'filter':
    with open('cohesion.json', 'r') as f:
        types = json.load(f)
    with open('filtered.json', 'w') as f:
        for type, data in types.items():
            if data['count'] < 10:
                continue
            f.write(type+' ('+str(data['count'])+'):\n')
            for tag in list(data['tags'].keys())[:5]:
                f.write('    '+tag+': '+str(round(data['tags'][tag], 2))+'%\n')