import json
import psycopg2
import random

def show_codex(commander_name):
    conn = psycopg2.connect("dbname='ddb' user='ddb' host='localhost' password='ddb'")
    cur = conn.cursor()
    cur.execute("select * from decks where commander='"+commander_name.replace('\'', '\'\'')+"';")
    decks = cur.fetchall()
    cur.close()
    conn.close()

    differences = []
    for deck in decks:
        for deck2 in decks:
            differences.append(len(set(deck2[2]).symmetric_difference(set(deck[2])))/2)
    commander_avg_difference = sum(differences)/len(differences)

    avg_limit = 20

    def filter(decks):
        deck_groups = []
        for deck in decks:
            if deck_groups == []:
                deck_groups.append([deck])
            else:
                group_distances = []
                for i, group in enumerate(deck_groups):
                    distances = []
                    for deck2 in group:
                        distance = len(set(deck2[2]).symmetric_difference(set(deck[2])))/2
                        distances.append(distance)
                    group_distances.append(sum(distances)/len(distances))
                closest_distance = min(group_distances)
                closest_group = group_distances.index(closest_distance)
                if closest_distance > avg_limit:
                    deck_groups.append([deck])
                else:
                    deck_groups[closest_group].append(deck)

        biggest_group = []
        biggest_index = None
        for i, group in enumerate(deck_groups):
            if len(group) > len(biggest_group):
                biggest_group = group
                biggest_index = i

        other_group = []
        for i, group in enumerate(deck_groups):
            if i == biggest_index:
                continue
            for deck in group:
                other_group.append(deck)

        main_cards = {}
        for deck in biggest_group:
            for card in deck[2]:
                if card not in main_cards:
                    main_cards[card] = 0
                main_cards[card] += 1
        
        pet_cards = []
        for card, count in main_cards.items():
            if count == 1:
                pet_cards.append(card)

        repeat = False
        for deck in other_group:
            for deck2 in other_group:
                if deck[0] != deck2[0]:
                    distance = len(set(deck2[2]).symmetric_difference(set(deck[2])))/2
                    if distance <= avg_limit:
                        repeat = True 
        print(len(biggest_group), len(other_group), len(pet_cards), repeat)
        return biggest_group, other_group, pet_cards, repeat

    groups = []
    biggest_group, other_group, pet_cards, repeat = filter(decks)
    groups.append({'decks': biggest_group, 'pet_cards': pet_cards})
    while repeat:
        biggest_group, other_group, pet_cards, repeat = filter(other_group)
        groups.append({'decks': biggest_group, 'pet_cards': pet_cards})
    group_counts = []
    for group in groups:
        group_counts.append(len(group['decks']))

    filter_size = sum(group_counts)/len(group_counts)

    filtered_groups = []
    for group in groups:
        if len(group['decks']) >= filter_size:
            cards = {}
            for deck in group['decks']:
                for card in deck[2]:
                    if card not in cards:
                        cards[card] = 0
                    cards[card] += 1
            group['cards'] = cards
            filtered_groups.append(group)

    for group in filtered_groups:
        group['percents'] = {}
        for card, count in group['cards'].items():
            group['percents'][card] = count/len(group['decks'])*100

    for group in filtered_groups:
        group['updated_percents'] = {}
        for card, count in group['percents'].items():
            if len(filtered_groups) == 1:
                group['updated_percents'][card] = count
            else:
                for group2 in filtered_groups:
                    if group != group2:
                        if card in group2['percents']:
                            group['updated_percents'][card] = count - group2['percents'][card]
                        else:
                            group['updated_percents'][card] = count
                        
    for group in filtered_groups:
        if len(group['decks']) == 1 or len(list(set(list(group['percents'].values())))) == 1 or len(filtered_groups) == 1:
            group['defining_cards'] = []
            continue
        avg_distances = {}
        for card, percent in group['updated_percents'].items():
            if len(filtered_groups) == 1:
                avg_distances[card] = percent
            else:
                distances = []
                for group2 in filtered_groups:
                    if group != group2:
                        if card in group2['updated_percents']:
                            distances.append(percent)
                        else:
                            distances.append(percent)
                avg_distances[card] = sum(distances)/len(distances)
        avg_distances = {k: v for k, v in reversed(sorted(avg_distances.items(), key=lambda item: item[1]))}
        highest_distance = list(avg_distances.values())[0]
        group['defining_cards'] = []
        while avg_distances[list(avg_distances.keys())[0]] == highest_distance or len(group['defining_cards']) < 5:
            group['defining_cards'].append(list(avg_distances.keys())[0])
            avg_distances.pop(list(avg_distances.keys())[0])

    if '//' in commander_name:
        commander_name = commander_name.split('//')[0].strip()
    with open('output/'+commander_name+'.txt', 'w') as f:
        for i, group in enumerate(filtered_groups):
            f.write('Build '+str(i+1)+'\n')
            miss = 1000
            while miss < 2:
                deck = random.choice(group['decks'])
                miss = 0
                for card in group['defining_cards']:
                    if card not in deck[2]:
                        miss += 1
            f.write('    Example Deck: '+deck[0]+'\n')
            f.write('    Defining Cards:\n')
            for card in group['defining_cards']:
                f.write('        '+card+'\n')
            #for card, percent in group['updated_percents'].items():
            #    f.write(card+' '+str(percent)+'%\n')

conn = psycopg2.connect("dbname='ddb' user='ddb' host='localhost' password='ddb'")
cur = conn.cursor()
cur.execute("select distinct commander from decks;")
commanders = cur.fetchall()
cur.close()
conn.close()

show_codex('')