import json
import requests
import time
import urllib.parse

r = requests.get('https://api2.moxfield.com/v1/hubs?pageNumber=1&pageSize=200')
data = r.json()

hub_data = {}

for hub in data['data']:
    print(hub['name'])
    r = requests.get('https://api2.moxfield.com/v2/decks/search?pageNumber=1&pageSize=64&sortType=updated&sortDirection=Descending&filter=&fmt=commander&hubName='+urllib.parse.quote_plus(hub['name']))
    data = r.json()
    hub_data[hub['name']] = data['totalResults']
    time.sleep(2)
with open('hub_counts.json', 'w') as f:
    f.write(json.dumps(hub_data, indent=4))