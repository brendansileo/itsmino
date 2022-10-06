import sys
import json
import re
sys.path.insert(0, '../api')
import mtg_api
from definer import define

def define_card(card_name, card):
    definition = {'name': card_name}
    if 'Dungeon' in card['types'] or 'commander' not in card['legalities'] or card['legalities']['commander'].lower() != 'legal' or '//' in card_name:
        return None

    definition['types'] = card['supertypes'] + card['types']
    definition['subtypes'] = card['subtypes']

    color_identity = ''.join(card['colorIdentity'])
    definition['color_identity'] = color_identity
    
    raw_oracle_text = card['text'] if 'text' in card else ''
    definition['raw_oracle_text'] = raw_oracle_text
    
    filtered_oracle_text = re.sub('\(.*\)', '', raw_oracle_text.lower())
    definition['abilities'] = define(card_name.lower(), card, filtered_oracle_text)
    
    return definition