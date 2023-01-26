import json
import requests
import sys
import time
sys.path.insert(0, '../api')
import mtg_api

r = requests.get('http://raw.githubusercontent.com/AverageDragon/cEDH-Decklist-Database/master/_data/database.json')
data = r.json()

all_lists = []

for entry in data:
    if entry['section'] not in ['BREW', 'COMPETITIVE']:
            continue
    for link in entry['decklists']:
            all_lists.append(link['link'].strip())

deck_data = {}
skipped = []
for i, url in enumerate(all_lists):
    print(url)
    try:
        deck = mtg_api.get_deck(url)
        deck_data[url] = deck.get_deck()
    except:
        skipped.append(url)
    print(i, len(all_lists))
    time.sleep(2)
print(skipped)
with open('decks.json', 'w') as f:
    f.write(json.dumps(deck_data,indent=4))
