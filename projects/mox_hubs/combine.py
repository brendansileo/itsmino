import json
import os

all_decks = {}

files = os.listdir('comp_decks')
for file in files:
    print(file)
    with open('comp_decks/'+file, 'r') as f:
        data = json.load(f)
    for url, info in data.items():
        all_decks[url] = info
with open('all_decks.json', 'w') as f:
    f.write(json.dumps(all_decks, indent=4))