import sys
import re


def is_ramp(text):
    text = text.lower()
    if re.search('add {[cwubrg]}', text) != None:
        return True
    if re.search('add .*? mana', text) != None:
        return True
    if re.search('untap .*? (forest|island|swamp|plains|mountain|land|permanent|artifact)', text) != None:
        return True
    if re.search('create .*? treasure', text) != None:
        return True
    if re.search('adds an additional', text) != None:
        return True
def get_speed(deck):
    commander_info = deck.get_commander_info()
    commander_mvs = []
    for commander, info in commander_info.items():
        commander_mvs.append(info['card']['cmc'])
    average_commander_mv = sum(commander_mvs)/len(commander_mvs)

    decklist = deck.get_decklist()
    card_mvs = []
    ramp_count = 0
    ramp_costs = []
    for card, info in decklist.items():
        if 'Land' not in info['card']['type_line']:
            if info['card']['layout'] != 'normal':
                oracle_text = ''
                #get mv of cards
                card_mvs.append(info['card']['cmc']/2)
                for face in info['card']['card_faces']:
                    #get ramp
                    oracle_text += face['oracle_text']
                if is_ramp(oracle_text):
                    ramp_count += 1
                    ramp_costs.append(info['card']['cmc']/2)
            else:
                #get mv of cards
                card_mvs.append(info['card']['cmc'])
                #get ramp
                if is_ramp(info['card']['oracle_text']):
                    ramp_count += 1
                    ramp_costs.append(info['card']['cmc'])
    average_card_mv = sum(card_mvs)/len(card_mvs)
    average_ramp_mv = sum(ramp_costs)/len(ramp_costs)

    score = ramp_count - (average_card_mv*3 + average_ramp_mv*2)

    print("""
-Speed of Setup-

Commander MV: {commander_mv}

Average MV: {avg_mv}

Ramp Count: {ramp_count}
Average Ramp MV: {avg_ramp_mv}
    """.format(name=deck.get_name(),
            commander='/'.join(deck.get_commander()),
            commander_mv=average_commander_mv,
            avg_mv=average_card_mv,
            ramp_count=ramp_count, 
            avg_ramp_mv=average_ramp_mv))
    return score