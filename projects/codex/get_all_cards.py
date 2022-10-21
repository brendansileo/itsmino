from gc import collect
import json
import os
import prices_api
import time

start = time.time()

files = os.listdir('comp_decks')

cards = []
for file in sorted(files):
    print(file)
    with open('comp_decks/'+file, 'r') as f:
        decks = json.load(f)
    for url, deck in decks.items():
        for card in deck['mainboard']:
            if card not in cards:
                cards.append(card)

with open('cards.json', 'w') as f:
    f.write(json.dumps(cards, indent=4))

card_prices = {}

for i, card in enumerate(cards):
    print(i, card)
    card_prices[card] = prices_api.get_card_price(card)
    time.sleep(1)

with open('card_prices.json', 'w') as f:
    f.write(json.dumps(card_prices, indent=4))
"""
with open('card_prices.json', 'r') as f:
    card_prices = json.load(f)
"""
for file in sorted(files):
    print(file)
    with open('comp_decks/'+file, 'r') as f:
        decks = json.load(f)

    deck_prices = {}

    for url, deck in decks.items():
        print(url)
        price = prices_api.get_price(deck['mainboard'], card_prices)
        deck['price'] = price
        deck_prices[url] = deck

    with open('comp_deck_prices/'+file, 'w') as f:
        f.write(json.dumps(deck_prices, indent=4))

print(time.time()-start)