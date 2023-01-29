import copy
import time
import sys
import json
sys.path.insert(0, '../api')
import mtg_api

output = []
data = {'tournament_name': 'Okotoberfest 2022', 'attendents': 144, 'date': '11-18-2022'}
with open('oko_urls.txt', 'r') as f:
    lines = f.readlines()
for line in lines:
    print(line)
    split = line.split(': ')
    standing = split[0]
    url = split[1]
    temp = copy.deepcopy(data)
    temp['standing'] = int(standing)
    deck = mtg_api.get_deck(url).get_deck()
    temp['deck'] = deck
    output.append(temp)
    time.sleep(2)

with open('eminence/oko.json', 'w') as f:
    json.dump(output, f, indent=4)