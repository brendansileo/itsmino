import requests
import framework
import json

r = requests.get('https://mtgjson.com/api/v5/AtomicCards.json')
all_cards = r.json()['data']

ramps = []
counters = []

def is_ramp(ability_type, ability):
    if ability == None or type(ability) == str:
        return False
    if ability['effect'] != None:    
        for effect in ability['effect']:
            if effect['action'] == 'add mana' or (effect['action'] == 'search' and 'land' in effect['details']['target'] and 'battlefield' in effect['details']['location']):
                return True

def is_counters(ability_type, ability):
    if ability == None or type(ability) == str:
        return False
    if ability['effect'] != None:    
        for effect in ability['effect']:
            if effect['action'] == 'remove counters' or effect['action'] == 'put counters':
                return True

for card, info in all_cards.items():
    print(card)
    if 'Land' in info[0]['types']:
        continue
    definition = framework.define_card(card, info[0])
    if card == 'Ageless Entity':
        print(definition)
        exit()
    if not definition:
        continue
    for ability_type, abilities in definition['abilities'].items():
        for ability in abilities:
            if is_ramp(ability_type, ability):
                ramps.append(card)
                break
            if is_counters(ability_type, ability):
                counters.append(card)
                break

print(json.dumps(counters, indent=4))
print(len(counters))
