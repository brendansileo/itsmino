import json
import sys
sys.path.insert(0, '../power_level')
import powerlevel

with open('comp_decklists.json', 'r') as f:
    moxlists = json.load(f)

power_levels = {}
i = 0
for url, deck in moxlists.items():
    print(i)
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