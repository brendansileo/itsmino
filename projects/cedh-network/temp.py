import json

with open('ddb_decks.json', 'r') as f:
    data = json.load(f)

warriors = []
for deck, info in data.items():
    mainboard = info['mainboard']
    for card, card_info in mainboard.items():
        if 'card_faces' not in card_info:
            if 'Warrior' in card_info['card']['type_line']:
                warriors.append(card)
print(set(warriors))