import json
import sys
import os
sys.path.insert(0, '../power_level')
import powerlevel

files = os.listdir('comp_decks')
power_levels = {}
for file in files:
    print(file)
    with open('comp_decks/'+file, 'r') as f:
        moxlists = json.load(f)
    i = 0
    for url, deck in moxlists.items():
        level = powerlevel.rate(deck['decklist'])
        if level in ['HIGH', 'MAX']:
            level = 'Competitive'
        else:
            level = 'Casual'
        if level not in power_levels:
            power_levels[level] = 0
        power_levels[level] += 1
        i += 1
    print(power_levels)