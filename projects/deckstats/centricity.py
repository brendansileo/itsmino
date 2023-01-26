import json
import spellbook

with open('decks.json', 'r') as f:
    decks = json.load(f)

all_cards = {}
percent_commander_combos = {}
deck_combos = {}
url_commanders = {}
claimed_commanders = []
kept_decks = []
print('collecting data')
count = 1
for url, deck in decks.items():
    print(count, len(decks))
    count += 1
    if 'mainboard' in deck and ';'.join(deck['commanders']) not in claimed_commanders:
        claimed_commanders.append(';'.join(deck['commanders']))
        kept_decks.append(url)
        for card in deck['mainboard']:
            if card not in all_cards:
                all_cards[card] = 0
            all_cards[card] += 1

        claimed_cards = []
        url_commanders[url] = ';'.join(deck['commanders'])
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
        deck_combos[url] = filtered_combos
        commander_combos = []
        for combo in filtered_combos:
            keep = False
            for card in combo:
                if card in deck['commanders']:
                    keep = True        
            if keep:
                commander_combos.append(combo)  
        if 
        try:
            percent_commander_combos[url] = len(commander_combos)/len(filtered_combos)
        except ZeroDivisionError:
            percent_commander_combos[url] = 0
            
print('filtering data')
num_decks = len(decks)

unique_cards = []
for card, frequency in all_cards.items():
    if frequency < num_decks*.01:
        unique_cards.append(card)

unique_count = {}
for url, deck in decks.items():
    if url in kept_decks:
        unique_count[url] = 0
        for card in deck['mainboard']:
            if card in unique_cards:
                unique_count[url] += 1
            
final = {}
print('finilizing data')
for url, count in unique_count.items():
    final[url] = {'commander': url_commanders[url], 'uniqueness': count, 'combo_multiplier': percent_commander_combos[url], 'combos': deck_combos[url], 'total': count * percent_commander_combos[url]}

with open('commander_centricity.json', 'w') as f:
    f.write(json.dumps({k: v for k, v in reversed(sorted(final.items(), key=lambda item: item[1]['total']))},indent=4))