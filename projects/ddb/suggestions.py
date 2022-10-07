from audioop import avg
import json
import psycopg2

commander_name = 'Yuriko, the Tiger\'\'s Shadow'

conn = psycopg2.connect("dbname='ddb' user='ddb' host='localhost' password='ddb'")
cur = conn.cursor()
cur.execute("select * from decks where commander='"+commander_name+"';")
decks = cur.fetchall()


differences = []
for deck in decks:
    for deck2 in decks:
        differences.append(len(set(deck2[2]).symmetric_difference(set(deck[2])))/2)
commander_avg_difference = sum(differences)/len(differences)

avg_limit = 15
pet_limit = 20

def filter(decks):
    deck_groups = []
    for deck in decks:
        if deck_groups == []:
            deck_groups.append([deck])
        else:
            group_distances = []
            for i, group in enumerate(deck_groups):
                distances = []
                for x, deck2 in enumerate(group):
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

    pet_cards_group = []
    other_group = []
    for i, group in enumerate(deck_groups):
        if i == biggest_index:
            continue
        for deck in group:
            distances = []
            for deck2 in biggest_group:
                distance = len(set(deck2[2]).symmetric_difference(set(deck[2])))/2
                distances.append(distance)
            avg_distance = sum(distances)/len(distances)
            if avg_distance > pet_limit:
                other_group.append(deck)
            else:
                pet_cards_group.append(deck)

    main_cards = []
    for deck in biggest_group:
        for card in deck[2]:
            main_cards.append(card)

    pet_cards = []
    for deck in pet_cards_group:
        for card in deck[2]:
            if card not in main_cards and card not in pet_cards:
                pet_cards.append(card)

    repeat = False
    for deck in other_group:
        for deck2 in other_group:
            if deck[0] != deck2[0]:
                distance = len(set(deck2[2]).symmetric_difference(set(deck[2])))/2
                if distance <= avg_limit:
                    repeat = True 
    print(len(biggest_group), len(pet_cards_group), len(other_group), len(pet_cards), repeat)
    return biggest_group, pet_cards_group, other_group, pet_cards, repeat

groups = []
biggest_group, pet_cards_group, other_group, pet_cards, repeat = filter(decks)
groups.append({'main': biggest_group, 'secondary': pet_cards_group, 'pet_cards': pet_cards})
while repeat:
    biggest_group, pet_cards_group, other_group, pet_cards, repeat = filter(other_group)
    groups.append({'main': biggest_group, 'secondary': pet_cards_group, 'pet_cards': pet_cards})

with open('output/'+commander_name+'.txt', 'w') as f:
    for group in groups:
        f.write('~~~~~\n')
        for g, decks in group.items():
            f.write('    '+g+'\n')
            for deck in decks:
                if g == 'pet_cards':
                    f.write('        '+deck+'\n')
                else:
                    f.write('        '+deck[0]+'\n')
    f.write('~~~~other decks~~~~\n')
    for deck in other_group:
        f.write('    '+deck[0]+'\n')
"""    
    f.write('~~~~~~average builds~~~~~~\n')
    for deck in biggest_group:
        f.write('    '+deck[0]+'\n')
    f.write('~~~~~~pet cards build~~~~~~\n')
    for deck in pet_cards_group:
        f.write('    '+deck[0]+'\n')
    f.write('~~~~~~other builds~~~~~~\n')
    for deck in other_group:
        f.write('    '+deck[0]+'\n')
    f.write('~~~~~~pet cards~~~~~~\n')
    for card in pet_cards:
        f.write('    '+card+'\n')
"""