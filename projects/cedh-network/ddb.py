import json
import requests
import time
import sys
sys.path.insert(0, '../api')
import mtg_api

r = requests.get('http://raw.githubusercontent.com/AverageDragon/cEDH-Decklist-Database/master/_data/database.json')
data = r.json()

all_lists = {}
count = 0
for entry in data:
    if entry['section'] not in ['BREW', 'COMPETITIVE']:
        continue
    #for link in entry['decklists']:
    link = entry['decklists'][0]
    print(link['link'])
    deck = mtg_api.get_deck(link['link'])
    if deck != None:
        d = deck.get_deck()
        d_list = deck.get_decklist()
        d2 = {}
        for card, info in d_list.items():
            if 'Land' not in info['card']['type_line']:
                d2[card] = info
        d['mainboard'] = d2
        colors = entry['colors']
        colors.sort()
        all_lists[entry['title']] = {'deck':d, 'colors':''.join(colors)}
    else:
        print('non-moxfield')
    print(count)
    count += 1
    time.sleep(2)
with open('ddb_decks_entry.json', 'w') as f:
        f.write(json.dumps(all_lists, indent=4))
