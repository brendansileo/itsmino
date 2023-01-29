import os
import json
import psycopg2
import sys
sys.path.insert(0, '../api')
import mtg_api


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

decks = {}
top16s = {}
attendents = {}

files = os.listdir('eminence')
for file in files:
    with open('eminence/'+file, 'r') as f:
        data = json.load(f)
    for deck in data:
        if not deck['deck'] or 'traceId' in deck['deck']:
            continue
        commander = ';'.join(sorted(list(deck['deck']['commanders'].keys())))
        if commander == '':
            continue
        archetype = get_archetype(commander.split(';'), deck['deck']['mainboard'].keys())
        if archetype not in attendents:
            attendents[archetype] = []
        attendents[archetype].append(deck['attendents'])
        if archetype not in decks:
            decks[archetype] = [0, commander]
        decks[archetype][0] += 1
        if archetype not in top16s:
            top16s[archetype] = 0
        if deck['standing'] <= 16:
            top16s[archetype] += 1

avg_attendents = {}
for archetype, counts in attendents.items():
    avg_attendents[archetype] = sum(counts)/len(counts)

conn = psycopg2.connect("dbname='cedh' user='pi' host='localhost' password='password'")
cur = conn.cursor()
cur.execute('drop table if exists tiers')
cur.execute('create table tiers (id serial primary key, commander text, count int, top16s int, attendents int, image text)')

for archetype, data in decks.items():
    count = data[0]
    commander = data[1]
    cur.execute('insert into tiers(commander, count, top16s, attendents, image) values (\''+archetype.replace('\'', '\'\'')+'\', '+str(count)+', '+str(top16s[archetype])+', '+str(avg_attendents[archetype])+', \''+mtg_api.get_picture(commander.split(';')[0], 'art_crop')+'\');')

conn.commit()
cur.close()
conn.close()