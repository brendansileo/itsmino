import json

with open('comp_decklists.json', 'r') as f:
    moxlists = json.load(f)

commanders = {}
for url, deck in moxlists.items():
    c = ';'.join(deck['commander'])
    if c == '':
        print(url)
    if c not in commanders:
        commanders[c] = 0
    commanders[c] += 1
commanders = {k: v for k, v in reversed(sorted(commanders.items(), key=lambda item: item[1]))}

"""
i = 0
c = len(commanders)
while i < c:
    clist = list(commanders.keys())
    commander = clist[i]
    i += 1
"""
#print(commanders['Rionya, Fire Dancer'])