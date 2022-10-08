import json
import os
import psycopg2

files = os.listdir('comp_decks')

#conn = psycopg2.connect("dbname='ddb' user='ddb' host='localhost' password='ddb'")
conn = psycopg2.connect("dbname='cedh' user='pi' host='localhost' password='password'")
cur = conn.cursor()
cur.execute("drop table if exists moxfield_decks;")
cur.execute("create table moxfield_decks (url text, commander text, decklist json);")

for file in sorted(files):
    print(file)
    with open('comp_decks/'+file, 'r') as f:
        decks = json.load(f)
    
    for url, deck in decks.items():
        cur.execute('INSERT into moxfield_decks (url, commander, decklist) VALUES (\''+url+'\', \''+';'.join(sorted(deck['commander'])).replace('\'', '\'\'')+'\', \''+json.dumps(deck['decklist']).replace('\'', '\'\'')+'\');')

conn.commit()
cur.close()
conn.close()