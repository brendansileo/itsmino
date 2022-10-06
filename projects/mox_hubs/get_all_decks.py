import sys
import requests
import time
import json
sys.path.insert(0, '../api')
import mtg_api

#started on 9/30/22

url = 'https://api2.moxfield.com/v2/decks/search?pageNumber={page}&pageSize=64&sortType=created&sortDirection=Ascending&fmt=commander&filter='
r = requests.get(url.format(page='1')).json()
total_pages = r['totalPages']
full_count = 0
tagged_count = 0
for i in range(total_pages):
    if i < 100:
        continue
    hubdata = []
    i += 1
    print(i, url.format(page=str(i)))
    r = requests.get(url.format(page=str(i))).json()
    data = r['data']
    for x, item in enumerate(data):
        print(x)
        deck = mtg_api.get_deck(item['publicUrl'])
        hubdata.append(deck.get_deck())
        time.sleep(2)
    with open('all_decks/page'+str(i)+'.json', 'w') as f:
        f.write(json.dumps(hubdata, indent=4))

print(full_count)
print(tagged_count)
        
            