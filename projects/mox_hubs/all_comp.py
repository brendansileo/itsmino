import sys
import os
import requests
import time
import json
sys.path.insert(0, '../api')
import mtg_api

#ran on 10/5/22

comp_hub_url = 'https://api2.moxfield.com/v2/decks/search?pageNumber={page}&pageSize=64&sortType=created&sortDirection=Ascending&fmt=commander&hubName=Competitive&board=mainboard'
r = requests.get(comp_hub_url.format(page='1')).json()
total_pages = r['totalPages']
for i in range(total_pages):
    i += 1
    print(comp_hub_url.format(page=str(i)))
    r = requests.get(comp_hub_url.format(page=str(i))).json()
    data = r['data']
    decklists = {}
    count = 0
    for item in data:
        print(str(count))
        print(item['publicUrl'])
        if item['mainboardCount'] != 100:
            continue
        deck = mtg_api.get_deck(item['publicUrl'])
        decklists[item['publicUrl']] = {'decklist':deck.get_decklist(), 'commander':deck.get_commander(), 'created':item['createdAtUtc'], 'updated':item['lastUpdatedAtUtc']}
        count += 1
        time.sleep(2)

    with open('comp_decks/comp_decklists{page}.json'.format(page=str(i)), 'w') as f:
        f.write(json.dumps(decklists, indent=4))