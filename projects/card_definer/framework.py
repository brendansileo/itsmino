import sys
import yake
import json
sys.path.insert(0, '../api')
import mtg_api
from definer import define

def define_card(card_name):
    definition = {'name': card_name}

    card = mtg_api.get_card(card_name)

    type_line = card['type_line'].split('—')
    types = type_line[0].strip().split(' ')
    subtypes = type_line[1].strip().split(' ') if '—' in card['type_line'] else None
    definition['types'] = types
    definition['subtypes'] = subtypes

    color_identity = card['color_identity']
    definition['color_identity'] = color_identity

    raw_oracle_text = card['oracle_text']
    definition['raw_oracle_text'] = raw_oracle_text
    
    definition['abilities'] = define(card_name.lower(), card, raw_oracle_text.lower())
    
    return definition

if __name__ == '__main__':
    card_name = ' '.join(sys.argv[1:])
    definition = define_card(card_name)
    print(json.dumps(definition, indent=4))