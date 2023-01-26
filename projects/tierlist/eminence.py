import requests
import json
import datetime
import time
import os
import psycopg2
import sys
sys.path.insert(0, '../api')
import mtg_api

mode = sys.argv[1]

def get_ddb_commanders(deck):
    commanders = []
    commanders.append(deck[list(deck.keys())[0]]['Commander/s'])
    c2 = deck[list(deck.keys())[1]]['Commander/s']
    if c2 != '':
        commanders.append(c2)
    return sorted(commanders)

def get_archetype(commanders, deck):
    with open('data.json', 'r') as f:
        ddb_lists = json.loads(f.read())
    scores = {}
    for section, entries in ddb_lists.items():
        for entry, lists in entries.items():
            for ddb_name, ddb_list in lists['lists'].items():
                if get_ddb_commanders(ddb_list) != commanders:
                    continue
                if entry not in scores:
                    scores[entry] = len(set(deck)-(set(ddb_list.keys())))
                else:
                    score = len(set(deck)-(set(ddb_list)))
                    if score < scores[entry]:
                        scores[entry] = score

    sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    if len(sorted_scores) == 0:
        return ';'.join(commanders)
    closest = list(sorted_scores.keys())[0]
    if sorted_scores[closest] > 25:
        return ';'.join(commanders)
    else:
        return closest

if mode == 'load':
    url = 'https://eminence.events/api'
    headers= {'Authorization': 'iMVJ2KjbvxmghZDt9Xn0WL'}
    data = {'last': 100, 'columns': ['decklist', 'wins', 'losses', 'draws']}
    res = requests.post(url, data=data, headers=headers)
    data = res.json()
    files = os.listdir('eminence')

    for tournament in data:
        decks = []
        name = tournament['tournamentName']
        if name.replace(' ', '_').replace('/', '')+'.json' in files:
            continue
        print(name)
        date = datetime.datetime.fromtimestamp(tournament['dateCreated'])
        date = date.strftime('%m-%d-%Y')
        for i, deck in enumerate(tournament['standings']):
            if deck['decklist'] == '':
                continue
            print('    '+deck['decklist'])
            try:
                deck_data = mtg_api.get_deck(deck['decklist']).get_deck()
            except AttributeError:
                print('    skipped')
                continue
            decks.append({'tournament_name': name, 'attendents': len(tournament['standings']), 'date': date, 'deck': deck_data, 'wins': deck['wins'], 'losses': deck['losses'], 'draws': deck['draws'], 'standing': i+1})
            time.sleep(3)
        if len(decks) > 0:
            with open('eminence/'+name.replace(' ', '_').replace('/','')+'.json', 'w') as f:
                f.write(json.dumps(decks, indent=4))
 
if mode == 'db':
    conn = psycopg2.connect("dbname='cedh' user='pi' host='localhost' password='password'")
    cur = conn.cursor()
    cur.execute('drop table if exists eminence_decks')
    cur.execute('drop table if exists eminence_top16s')
#    cur.execute('drop table if exists eminence_cards')
    cur.execute('create table eminence_decks (name text, tournament text, date date, standing int, commander text);')
    cur.execute('create table eminence_top16s (name text, tournament text, date date, standing int, commander text);')
#    cur.execute('create table eminence_cards (card_name text, deck text, type')

    files = os.listdir('eminence')
    for file in files:
        with open('eminence/'+file, 'r') as f:
            data = json.load(f)
            for deck in data:
                try:
                    if 'title' not in deck['deck'] and ';'.join(list(deck['deck']['commanders'].keys())) == '':
                        print(deck['deck']['publicUrl'])
                except Exception as e:
                    print(e)
                    print(deck)
                    continue
                if 'title' in deck['deck'] and deck['deck']['title'] == 'Not Found':
                   continue
                archetype = get_archetype(sorted(list(deck['deck']['commanders'].keys())), deck['deck']['mainboard'].keys())
                cur.execute('INSERT into eminence_decks(name, tournament, date, standing, commander) VALUES (\''+deck['deck']['name'].replace('\'', '\'\'')+'\', \''+deck['tournament_name'].replace('\'', '\'\'')+'\', \''+deck['date']+'\', '+str(deck['standing'])+', \''+archetype.replace('\'', '\'\'')+'\');')
                if deck['standing'] <= 16:
                    cur.execute('INSERT into eminence_top16s(name, tournament, date, standing, commander) VALUES (\''+deck['deck']['name'].replace('\'', '\'\'')+'\', \''+deck['tournament_name'].replace('\'', '\'\'')+'\', \''+deck['date']+'\', '+str(deck['standing'])+', \''+archetype.replace('\'', '\'\'')+'\');')

    conn.commit()
    cur.close()
    conn.close()