import requests
import psycopg2
import json

r = requests.get('https://mtgjson.com/api/v5/AtomicCards.json')
all_cards = r.json()['data']

with open('config.json', 'r') as f:
    config = json.load(f)

conn = psycopg2.connect("dbname='"+config['db_name']+"' user='"+config['username']+"' host='"+config['hostname']+"' password='"+config['password']+"'")
cur = conn.cursor()
cur.execute("drop table if exists "+config['table_name']+";")
cur.execute("create table "+config['table_name']+" (card_name text, colors text, color_identity text, mana_value int, mana_cost text, oracle_text text, types text);")

for card, data in all_cards.items():
    print(card)
    data = data[0]
    text = data['text'] if 'text' in data else ''
    cur.execute('INSERT into '+config['table_name']+'(card_name, colors, color_identity, mana_value, oracle_text, types) VALUES (\''+card.replace('\'', '\'\'')+'\', \''+''.join(data['colors'])+'\', \''+''.join(data['colorIdentity'])+'\', '+str(int(data['manaValue']))+', \''+text.replace('\'', '\'\'')+'\', \''+' '.join(data['types'])+'\');')

conn.commit()
cur.close()
conn.close()