import json
import random
import requests
import sys
sys.path.insert(0, '../api')
import mtg_api

def pick7():
    categories = {}
    r = requests.get('http://itsmino.tk/categories')
    for line in r.text.split('\n'):
        if line != '':
            line = line.split(';')
            categories[line[0]] = line[1].strip()

    r = requests.get('http://itsmino.tk/decks')
    decks = r.text
    chosen_deck = random.choice(decks.split('\n'))

    r = requests.get('http://itsmino.tk/decks/'+chosen_deck)
    decklist = r.json()

    full_decklist = []
    for card, info in decklist.items():
        for i in range(info['quantity']):
            full_decklist.append(card)

    hand = {}
    for i in range(7):
        card = random.choice(list(full_decklist))
        full_decklist.remove(card)
        if 'card_faces' not in card or len(card['card_faces']) == 0:
            info = decklist[card]['card']
        else:
            info = decklist[card]['card_faces'][0]
        hand[card] = {'category': categories[card], 'mv': info['cmc'], 'image': mtg_api.get_picture(card, 'small')}

    return chosen_deck, hand
