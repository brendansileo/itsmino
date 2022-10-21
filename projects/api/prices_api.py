import requests
import time

def get_card_price(card):
    lowest_price = 0
    r = requests.get('https://api.scryfall.com/cards/named?exact='+card.replace(' ','+'))
    p = r.json()
    card_prices = [p['prices']['usd'], p['prices']['usd_foil'], p['prices']['usd_etched']]
    for price in card_prices:
        if price != None:
            if lowest_price == 0:
                lowest_price = price
            elif float(price) < float(lowest_price):
                lowest_price = price
    return lowest_price

def get_deck_price(decklist, collected_prices):
    total_price = 0
    for card in decklist.keys():
        if card in collected_prices:
            lowest_price = collected_prices[card]
        else:
            print(card)
            lowest_price = 0
            r = requests.get('https://api.scryfall.com/cards/named?exact='+card.replace(' ','+'))
            prints_uri = r.json()['prints_search_uri']
            r = requests.get(prints_uri)
            prints = r.json()['data']
            lowest_price = 0
            for p in prints:
                if p['legalities']['commander'] != 'legal' or p['set_type'] == 'memorabilia':
                    continue
                card_prices = [p['prices']['usd'], p['prices']['usd_foil'], p['prices']['usd_etched']]
                for price in card_prices:
                    if price != None:
                        if lowest_price == 0:
                            lowest_price = price
                        elif float(price) < float(lowest_price):
                            lowest_price = price
            collected_prices[card] = lowest_price
        total_price += float(lowest_price)
    return total_price, collected_prices