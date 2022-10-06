import sys
import os
import requests
import time
import json
import urllib.parse

total_decks = 677308
#run on 10/5

r = requests.get('https://api2.moxfield.com/v1/hubs?pageNumber=1&pageSize=200')
data = r.json()

deck_data = {}

for hub in data['data']:
    print(hub['name'])
    url = 'https://api2.moxfield.com/v2/decks/search?pageNumber={page}&pageSize=64&sortType=created&sortDirection=Ascending&fmt=commander&filter=&hubName='+urllib.parse.quote_plus(hub['name'])
    r = requests.get(url.format(page='1')).json()
    total_pages = r['totalPages']
    for i in range(total_pages):
        x = i + 1
        print(url.format(page=str(x)))
        r = requests.get(url.format(page=str(x))).json()
        data = r['data']
        for deck in data:
            publicId = deck['publicId']
            if publicId not in deck_data:
                deck_data[publicId] = deck
                deck_data[publicId]['hubNames'] = []
            deck_data[publicId]['hubNames'].append(hub['name'])
        time.sleep(3)
    with open('hubs_deck_data.json', 'w') as f:
        f.write(json.dumps(deck_data, indent = 4))