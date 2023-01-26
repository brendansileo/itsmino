import requests
import json
import re
import urllib.request

class Deck:
    deck = None

    def __init__(self, deck_data):
        self.deck = deck_data

    def get_deck(self):
        if 'status' in self.deck and self.deck['status'] == 404:
            return None
        else:
            return self.deck

    def get_decklist(self):
        if 'mainboard' in self.deck:
            return self.deck['mainboard']
        else:
            return None

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
    
    username = 'cedh_guide'
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
    
    username = 'cedh_guide'
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

def make_text_deck(name, commanders, decklist):
    username = 'cedh_guide'
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
        'mainboard':decklist,
        'name':name, 
        'maybeboard': '',
        'playStyle': 'paperDollars',
        'pricingProvider': 'tcgplayer',
        'sideboard': '',
        'visibility': 'unlisted'
    }

    r = requests.post('https://api2.moxfield.com/v2/decks', json=data, headers=headers).json()
    publicID = r['publicId']
    id = r['deck']['id']
    cardID = None
    partnerID = None
    for commander in commanders:
        r = requests.get('https://api2.moxfield.com/v2/cards/search?q='+commander.replace(' ', '+')+'+((is:commander+f:commander)+or+(is:commander+date%3E2023-01-21))').json()
        if cardID == None:
            cardID = r['data'][0]['id']
        else:
            partnerID = r['data'][0]['id']
    if partnerID:
        data = {'clearCommanders': True, 'commanderCardId': cardID, 'partnerCardId': partnerID}
    else:
        data = {'clearCommanders': True, 'commanderCardId': cardID}
    r = requests.put('https://api2.moxfield.com/v2/decks/'+id+'/commanders', json=data, headers=headers)
    return 'https://www.moxfield.com/decks/'+publicID
    
def get_mtggoldfish_deck(link):
    split_link = link.split('#')[0].split('/')
    deck_id = split_link[4]
    fp = urllib.request.urlopen('https://www.mtggoldfish.com/deck/'+deck_id)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    res = re.findall('<a href=\"/archetype/commander-.*?\">.*?</a>', mystr)
    commander = re.findall('(?<=>).*?(?=<)', res[0])[0]
    r = requests.get('https://www.mtggoldfish.com/deck/download/'+deck_id)
    decklist = r.text.split('\n')
    filter_decklist = []
    for line in decklist:
        if commander not in line:
            filter_decklist.append(line)
    filter_decklist = '\n'.join(filter_decklist)
    username = 'cedh_guide'
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
        'mainboard':filter_decklist,
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
    return Deck(requests.get('https://api.moxfield.com/v2/decks/all/'+link_id.strip()).json())

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
    r = requests.get('https://api.scryfall.com/cards/named?exact='+card_name.replace(' ','+').replace('&', '%26')).json()
    if 'image_uris' in r:
        return r['image_uris'][size]
    else:
        return r['card_faces'][0]['image_uris'][size]
