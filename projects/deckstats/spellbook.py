import json
import requests
import time
import sys
import psycopg2
import ast

def reload():
    r = requests.get('https://sheets.googleapis.com/v4/spreadsheets/1KqyDRZRCgy8YgMFnY0tHSw_3jC99Z0zFvJrPbfm66vA/values:batchGet?ranges=combos!A2:Q&key=AIzaSyBD_rcme5Ff37Evxa4eW5BFQZkmTbgpHew')
    combos = {}
    raw_combos = r.json()['valueRanges']
    for range in raw_combos:
        for value in range['values']:
            cards = value[1:11]
            cards = list(map(str.strip, cards))
            while('' in cards):
                cards.remove('')
            for card in cards:
                card = card.strip()
                if card not in combos:
                    combos[card] = []
                color_identity = value[11].upper().split(',')
                combos[card].append((cards, color_identity, value[0]))

    with open('combos.json', 'w') as f:
        f.write(json.dumps(combos, indent=4))

def get_combo_color(combo):
    with open('combos.json', 'r') as f:
        combos = json.loads(f.read())
    card1 = combo[0]
    target_combos = combos[card1]
    for c in target_combos:
        if set(c[0]) == set(combo):
            return c[1]

def get_combo_id(combo):
    with open('combos.json', 'r') as f:
        combos = json.loads(f.read())
    card1 = combo[0]
    target_combos = combos[card1]
    for c in target_combos:
        if set(c[0]) == set(combo):
            return c[2]

def get_combos(decklist, commanders, allowed_distance):
    with open('combos.json', 'r') as f:
        combos = json.loads(f.read())
    color_identity = []
    for commander in commanders.values():
        color_identity += commander['card']['color_identity']
    color_identity = list(set(color_identity))
    decklist = list(decklist.keys())

    for commander in commanders:
        decklist.append(commander)

    results = {}
    for i in range(allowed_distance+1):
        results[str(i)] = []
    for card in decklist:
        if card in combos:
            for combo in combos[card]:
                skip = False
                for color in combo[1]:
                    if color not in color_identity:
                        skip = True
                if not skip:
                    distance = 0
                    for c in combo[0]:
                        if c not in decklist:
                            distance += 1
                    if distance <= allowed_distance:
                        add = True
                        for x in results[str(distance)]:
                            if set(combo[0]) == set(x):
                                add = False
                        if add:
                            results[str(distance)].append(combo[0])
    return(results)

if __name__ == '__main__':
    reload()
    mode = sys.argv[1]
    if mode == 'get':
        url = sys.argv[2]
        dist = int(sys.argv[3])
        print(get_combos(url, dist))
        exit()
    if mode == 'site':
        r = requests.get('http://raw.githubusercontent.com/AverageDragon/cEDH-Decklist-Database/master/_data/database.json')
        data = r.json()

        all_combos = {}

        for entry in data:
            if entry['section'] not in ['BREW', 'COMPETITIVE']:
                continue
            for link in entry['decklists']:
                print(link)
                try:
                    title, combos = get_combos(link['link'], 0)
                except:
                    continue
                for combo in combos['0']:
                    if str(combo) not in all_combos:
                        colors = get_combo_color(combo)
                        id = get_combo_id(combo)
                        all_combos[str(combo)] = {'colors': ''.join(colors), 'count': 0, 'decks': [], 'link': 'https://www.commanderspellbook.com/combo/'+id}
                    all_combos[str(combo)]['count'] += 1
                    all_combos[str(combo)]['decks'].append(entry['title']+':'+title)
                time.sleep(2)

        with open('deck_combos.json', 'w') as f:
            f.write(json.dumps(all_combos, indent=4))

    elif mode == 'file':
        with open('deck_combos.json', 'r') as f:
            all_combos = json.loads(f.read())

    conn = psycopg2.connect("dbname='cedh' user='pi' host='localhost' password='password'")
    cur = conn.cursor()
    cur.execute("drop table if exists combos;")
    cur.execute("create table combos (combo text, colors text, count int, decks text, link text);")
    for combo, info in all_combos.items():
        combo = ast.literal_eval(combo)
        combo = ' + '.join(combo)
        decks = ', '.join(info['decks'])
        cur.execute('INSERT into combos(combo, colors, count, decks, link) VALUES (\''+combo.replace('\'', '\'\'')+'\', \''+info['colors']+'\', '+str(info['count'])+', \''+decks.replace('\'', '\'\'')+'\', \''+info['link'].replace('\'', '\'\'')+'\');')

    conn.commit()
    cur.close()
    conn.close()
