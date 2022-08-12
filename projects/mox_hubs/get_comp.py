import sys
import requests
import time
import json
sys.path.insert(0, '../api')
import mtg_api

comp_hub_url = 'https://api2.moxfield.com/v2/decks/search?pageNumber=1&pageSize=1000&sortType=updated&sortDirection=Descending&hubName=Competitive&board=mainboard'
r = requests.get(comp_hub_url).json()

data = r['data']
decklists = {}
count = 0
for item in data:
    print(count)
    deck = mtg_api.get_deck(item['publicUrl'])
    decklists[item['publicUrl']] = deck.get_decklist()
    count += 1
    time.sleep(2)
with open('comp_decklists.json', 'w') as f:
    f.write(json.dumps(decklists, indent=4))