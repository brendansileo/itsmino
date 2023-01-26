import spellbook
import json

with open('decks.json', 'r') as f:
    decks = json.load(f)

spellbook.reload()
data = {}
count = 1
for url, deck in decks.items():
    print(count, len(decks))
    count += 1
    if 'mainboard' in deck:
        claimed_cards = []
        combos = spellbook.get_combos(deck['mainboard'], deck['commanders'], 0)['0']
        filtered_combos = []
        for combo in combos:
            keep = True
            for card in combo:
                if card in claimed_cards:
                    keep = False
                else:
                     claimed_cards.append(card)             
            if keep:
                filtered_combos.append(combo)  

        data[url] = {'commander': ';'.join(list(deck['commanders'].keys())), 'score': len(filtered_combos), 'combos': filtered_combos}

with open('resiliency.json', 'w') as f:
    f.write(json.dumps({k: v for k, v in reversed(sorted(data.items(), key=lambda item: item[1]['score']))},indent=4))