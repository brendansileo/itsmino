import requests
import json

class Deck:
    deck = None

    def __init__(self, deck_data):
        self.deck = deck_data

    def get_deck(self):
        return self.deck

    def get_decklist(self):
        return self.deck['mainboard']

    def get_commander(self):
        return list(self.deck['commanders'].keys())

    def get_commander_info(self):
        return self.deck['commanders']
    
    def get_format(self):
        return self.deck['format']

    def get_name(self):
        return self.deck['name']

def get_deck(link):
    if 'moxfield' not in link:
        return None
    if 'www' not in link:
        r = requests.get(link)
        link = r.url
    if link[-1] == '/':
            link = link[:-1]
    link_id = link.split('/')[-1]
    return Deck(requests.get('https://api.moxfield.com/v2/decks/all/'+link_id).json())

def get_card(card_name):
    return requests.get('https://api.scryfall.com/cards/named?exact='+card_name.replace(' ','+')).json()

def get_picture(card_name, size):
    return requests.get('https://api.scryfall.com/cards/named?exact='+card_name.replace(' ','+')).json()['image_uris'][size]