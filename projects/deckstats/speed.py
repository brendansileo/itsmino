import json
import re
from word2number import w2n

with open('decks.json', 'r') as f:
    data = json.load(f)

deck_nums = {}
for url, deck in data.items():
    deck = deck['mainboard']
    num_mana = 0
    for card, info in deck.items():
        if 'Land' in info['card']['type_line']:
            continue
        mv = info['card']['cmc']
        if info['card']['card_faces'] == []:
            oracle = info['card']['oracle_text'].lower()
        else:
            oracle = ''
            for face in info['card']['card_faces']:
                oracle += face['oracle_text']+';'
        matches = re.findall('(add (.* mana of any color|(\{[w|u|b|r|g|c|\d]\})+))', oracle)
        if len(matches) > 0:
            keep = False
            for match in matches:
                match = match[1]
                if '{' not in match:
                    num_word = match.split(' ')[0]
                    if w2n.word_to_num(num_word) > mv:
                        keep = True
                else:
                    m = re.findall('{.}', match)
                    if len(m) > mv:
                        keep = True
            if keep:
                num_mana += 1
    deck_nums[url] = num_mana

with open('speed.json', 'w') as f:
    f.write(json.dumps({k: v for k, v in reversed(sorted(deck_nums.items(), key=lambda item: item[1]))},indent=4))