import requests
import json
import re

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

def get_moxfield_import_deck(link):
    r = requests.post('https://api2.moxfield.com/v2/decks/remote-preview', json={"remoteUrl":link,"playStyle":"paperDollars","pricingProvider":"tcgplayer"})
    deck_import = r.json()
    
    username = 'cedhstats'
    password = 'cedh1234'

    headers={
        'Content-type':'application/json',
        'Accept':'application/json'
    }

    r = requests.post('https://api.moxfield.com/v1/account/token', json={'userName': username, 'password': password}, headers=headers)
    token = r.json()['access_token']

    headers = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'authorization':'Bearer '+ token
    }

    data = {
        'commanderCardId': deck_import['commander']['cardId'],
        'format': 'commander',
        'mainboard':deck_import['mainboard'],
        'name':deck_import['name'], 
        'maybeboard': '',
        'playStyle': 'paperDollars',
        'pricingProvider': 'tcgplayer',
        'sideboard': '',
        'visibility': 'public'
    }

    r = requests.post('https://api2.moxfield.com/v2/decks', json=data, headers=headers)
    r = r.json()['deck']
    deck = Deck(r)
    r = requests.delete('https://api2.moxfield.com/v1/decks/'+r['id'], headers=headers)
    return deck

def get_deckstats_deck(link):
    split_link = link.split('/')
    owner_id = split_link[4]
    deck_id = split_link[5].split('-')[0]
    url = 'https://deckstats.net/api.php?action=get_deck&id_type=saved&owner_id='+owner_id+'&id='+deck_id+'&response_type=list'
    r = requests.get(url)
    decklist = r.json()['list'].split('\n')
    filtered_decklist = {}
    commander = None
    for card in decklist:
        if card == '' or '//' in card:
            pass
        elif '!Commander' in card:
            card = card.split('#')[0].strip()
            card = re.sub('\[.*?\] ', '', card)
            commander = ' '.join(card.split(' ')[1:])
        else:
            card = card.split('#')[0].strip()
            card = re.sub('\[.*?\] ', '', card)
            split_card = card.split(' ')
            quantity, card_name = split_card[0], ' '.join(split_card[1:])
            if card_name not in filtered_decklist:
                filtered_decklist[card_name] = 0
            filtered_decklist[card_name] += int(quantity)
    deck_string = ''
    for card, quantity in filtered_decklist.items():
        deck_string += str(quantity)+' '+card+'\n'
    
    username = 'cedhstats'
    password = 'cedh1234'

    headers={
        'Content-type':'application/json',
        'Accept':'application/json'
    }

    r = requests.post('https://api.moxfield.com/v1/account/token', json={'userName': username, 'password': password}, headers=headers)
    token = r.json()['access_token']

    headers = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'authorization':'Bearer '+ token
    }

    data = {
        'commanderCardId': '',
        'format': 'commander',
        'mainboard':deck_string,
        'name':commander, 
        'maybeboard': '',
        'playStyle': 'paperDollars',
        'pricingProvider': 'tcgplayer',
        'sideboard': '',
        'visibility': 'public'
    }

    r = requests.post('https://api2.moxfield.com/v2/decks', json=data, headers=headers)
    r = r.json()['deck']
    r2 = requests.get('https://api.scryfall.com/cards/named?exact='+commander.replace(' ','+'))
    r['commanders'][commander] = r2.json()
    deck = Deck(r)
    r = requests.delete('https://api2.moxfield.com/v1/decks/'+r['id'], headers=headers)
    return deck

def get_moxfield_deck(link):
    if 'www' not in link:
        r = requests.get(link)
        link = r.url
    if link[-1] == '/':
            link = link[:-1]
    link_id = link.split('/')[-1]
    return Deck(requests.get('https://api.moxfield.com/v2/decks/all/'+link_id).json())

scrapers = {'moxfield': get_moxfield_deck, 'archidekt': get_moxfield_import_deck, 'tappedout': get_moxfield_import_deck, 'deckstats': get_deckstats_deck, 'mtggoldfish': get_mtggoldfish_deck}

def get_deck(link):
    for string, function in scrapers.items():
        if string in link:
            return function(link)
    return None

def get_deck_json(data):
    return Deck(data)

def get_card(card_name):
    return requests.get('https://api.scryfall.com/cards/named?exact='+card_name.replace(' ','+')).json()

def get_picture(card_name, size):
    return requests.get('https://api.scryfall.com/cards/named?exact='+card_name.replace(' ','+')).json()['image_uris'][size]
