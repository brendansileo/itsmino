import json
with open('decks.json', 'r') as f:
    decks = json.load(f)

results = {}

for i in range(0,3):
    print(i)
    results[i] = {}
    for url, deck in decks.items():
        results[i][url] = []
        for card, card_info in deck['mainboard'].items():
            try:
                if 'Land' in card_info['card']['type_line']:
                    continue
            except:
                pass
            if card_info['card']['cmc'] == i:
                results[i][url].append(card)
            elif 'power' in card_info['card']:
                if card_info['card']['power'] == str(i) or card_info['card']['toughness'] == str(i):
                    results[i][url].append(card)
    

with open('chiefresults.json', 'w') as f:
        for number in results:
            avg_count = 0
            results_number = {k: v for k, v in reversed(sorted(results[number].items(), key=lambda item: len(item[1])))}
            f.write(str(number)+':\n')
            for url, hits in results_number.items():
                avg_count += len(hits)
            f.write('    average number of hits: '+str(avg_count/len(results_number))+'\n')
            for url, hits in results_number.items():
                avg_count += len(hits)
                f.write('    '+url+', '+str(len(hits))+'\n')
                f.write('    '+', '.join(hits)+'\n')
