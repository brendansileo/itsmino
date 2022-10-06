import requests
import json

r = requests.get('https://api.scryfall.com/cards/search?q=t%3Aland+produces>1')
data = r.json()
lands = {}

def collect(cards, lands):
    for card in cards:
        types = card['type_line']
        types = types.split('//')
        skip = False
        if card['legalities']['commander'] == 'not_legal':
            skip = True
        for type in types:
            if 'Land' not in types:
                skip = True
        if not skip:
            if 'enters the battlefield tapped' in card['oracle_text']:
                tapped = 'yes'
                if 'unless' in card['oracle_text']:
                    tapped = 'conditional'
            else:
                tapped = 'no'
            lands[card['name']] = {'produces': card['produced_mana'], 'price': '$'+str(card['prices']['usd']), 'tapped': tapped, 'oracle': card['oracle_text']}
    return lands

lands = collect(data['data'], lands)
while 'next_page' in data:
	r = requests.get(data['next_page'])
	data = r.json()
	lands = collect(data['data'], lands)

with open('lands.json', 'w') as f:
    f.write(json.dumps(lands, indent=4))

print(len(list(lands.keys())))