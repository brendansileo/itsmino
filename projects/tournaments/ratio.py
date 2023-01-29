import os
import json

decks = {}
top16s = {}

files = os.listdir('eminence')
for file in files:
    print(file)
    with open('eminence/'+file, 'r') as f:
        data = json.load(f)
    for deck in data:
        if 'traceId' in deck['deck']:
            continue
        commander = ';'.join(sorted(list(deck['deck']['commanders'].keys())))
        if commander not in decks:
            decks[commander] = 0
        decks[commander] += 1
        if deck['standing'] <= 16:
            if commander not in top16s:
                top16s[commander] = 0
            top16s[commander] += 1

ratios = {}
for commander in decks.keys():
    ratios[commander] = 100*(top16s[commander]/decks[commander]) if commander in top16s else 0
ratios = {k: v for k, v in reversed(sorted(ratios.items(), key=lambda item: item[1]))}

for name, ratio in ratios.items():
    if top16s[name] <= 3: 
        continue
    if name == '':
        continue
    print(name+': ')
    print('    Registered: '+str(decks[name]))
    if name in top16s:
        print('    # in Top 16: '+str(top16s[name]))
    else:
        print('    # in Top 16: 0')
    print('    Turnover Rate: '+str(ratio)+'%')
