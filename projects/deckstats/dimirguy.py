import json
with open('decks.json', 'r') as f:
    decks = json.load(f)

results = {}

for i in range(0,3):
    print(i)
    results[i] = {}
    for url, deck in decks.items():
        results[i][url] = 0
        for card, card_info in deck['mainboard'].items():
            if card_info['card']['cmc'] == i:
                results[i][url] += 1
            elif 'power' in card_info['card']:
                if card_info['card']['power'] == i or card_info['card']['toughness'] == i:
                    results[i][url] += 1
    print(results)
    results[i] = {k: v for k, v in reversed(sorted(results[i].items(), key=lambda item: item[1]))}

with open('chiefresults.json', 'w') as f:
    json.dumps(results, indent=4)
