import requests
import json

class Deck:
    deck = None

    def __init__(self, deck_data):
        self.deck = deck_data

    def get_decklist(self):
        return self.deck['mainboard']

    def get_commander(self):
        return self.deck['commanders'].keys()

def get_deck(link):
    if link[-1] == '/':
            link = link[:-1]
    link_id = link.split('/')[-1]
    return Deck(requests.get('https://api.moxfield.com/v2/decks/all/'+link_id).json())

def get_card(card_name):
    return requests.get('https://api.scryfall.com/cards/named?exact='+card_name.replace(' ','+')).json()