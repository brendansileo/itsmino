import json
import os
import psycopg2
import sys
sys.path.insert(0, '../api')
import mtg_api

files = os.listdir('comp_decks')

conn = psycopg2.connect("dbname='ddb' user='ddb' host='localhost' password='ddb'")
cur = conn.cursor()
cur.execute("drop table if exists decks;")
cur.execute("create table decks (url text, commander text, decklist json, views int, has_primer text);")

for file in sorted(files):
    print(file)
    with open('comp_decks/'+file, 'r') as f:
        decks = json.load(f)
    
    for url, deck in decks.items():
        primer = 'No'
        for hub in deck['hubs']:
            if hub['name'] == 'Primer':
                primer = 'Yes'
        deck = mtg_api.get_deck_json(deck)
        cur.execute('INSERT into decks (url, commander, decklist, views, has_primer) VALUES (\''+url+'\', \''+';'.join(sorted(deck.get_commander())).replace('\'', '\'\'')+'\', \''+json.dumps(deck.get_decklist()).replace('\'', '\'\'')+'\', '+str(deck.get_deck()['viewCount'])+', \''+primer+'\');')

conn.commit()
cur.close()
conn.close()