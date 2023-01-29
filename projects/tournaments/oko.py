import json
import requests
import time
import sys
sys.path.insert(0, '../api')
import mtg_api

decks = {}
count = 0
dropped_standing = 10000
skipped = []
r = requests.get('http://157.245.1.243/api/v1/tournaments/past/all').json()
for key, values in r.items():
    for player in values['player_reg']['players']:
        for deck in player[1]['decks']:
            deck_string = ''
            commanders = []
            for card in deck[1]['mainboard']:
                deck_string += str(card[1])+' '+card[0]+'\n'
            for card in deck[1]['commanders']:
                commanders.append(card[0])
            standing = dropped_standing
            for i, score in enumerate(reversed(values['final_standings']['scores'])):
                if score[0] == player[0]:
                    standing = i+1
            if standing == dropped_standing:
                dropped_standing = dropped_standing + 1
            standing = str(standing)
            print('Oko '+standing+': '+'/'.join(commanders))
            decks[standing] = player[0]
            count += 1
            try:
                decks[standing] = mtg_api.make_text_deck('Oko '+standing+': '+'/'.join(commanders), commanders, deck_string)
            except:
                skipped.append(player[0])    
            time.sleep(2)
decks = dict(sorted(decks.items(), key=lambda x: int(x[0])))
with open('oko_urls.txt', 'w') as f:
    for standing, url in decks.items():
        f.write(standing+': '+url+'\n')
print('skipped: ', skipped)
