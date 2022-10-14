from calendar import c
import requests

def get_decks(group, name):
    final_decks = {}
    decks_by_views = list(reversed(sorted(group['decks'], key=lambda d: d[3])))
    final_decks['most viewed'] = decks_by_views[0][0]
    if decks_by_views[0][4] == 'No':
        primer_deck = None
        i = 1
        while primer_deck and primer_deck[4] == 'No':
            primer_deck = decks_by_views[i]
            i += 1
        final_decks['primer'] = primer_deck[0] if primer_deck else None
    else:
        final_decks['primer'] = final_decks['most viewed']

    r = requests.get('http://raw.githubusercontent.com/AverageDragon/cEDH-Decklist-Database/master/_data/database.json')
    data = r.json()

    all_links = {}
    for entry in data:
        if entry['section'] not in ['BREW', 'COMPETITIVE']:
            continue
        commanders = []
        for commander in entry['commander']:
            commanders.append(commander['name'])
        commander_name = ';'.join(sorted(commanders))
        for link in entry['decklists']:
            if commander_name not in all_links:
                all_links[commander_name] = []
            all_links[commander_name].append(link)

    ddb_link = None
    for link in all_links[name]:
        for deck in group['decks']:
            if link['link'][-1] == '/':
                link['link'] = link['link'][:-1]
            if link['link'] == deck[0]:
                ddb_link = link['link']
                break
    final_decks['ddb'] = ddb_link

    card_counts = {}
    for deck in group['decks']:
        for card in deck[2]:
            if card not in card_counts:
                card_counts[card] = 0
            card_counts[card] += 1
    
    average_deck = list({k: v for k, v in reversed(sorted(card_counts.items(), key=lambda item: item[1]))}.keys())[:100]

    smallest_distance = 1000
    smallest_distance_deck = None

    for deck in group['decks']:
        distance = len(set(deck[2].keys()).symmetric_difference(set(average_deck)))/2
        if distance < smallest_distance:
            smallest_distance = distance
            smallest_distance_deck = deck
            
    final_decks['average'] = smallest_distance_deck[0]

    return final_decks