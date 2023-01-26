import json

with open('decks.json', 'r') as f:
    data = json.load(f)

total = 0
breach_only = 0
oracle_only = 0
both = 0
either = 0

for url, deck in data.items():
    cards = deck['mainboard'].keys()
    if 'Underworld Breach' in cards and 'Thassa\'s Oracle' not in cards:
        breach_only += 1
    elif 'Thassa\'s Oracle' in cards and 'Underworld Breach' not in cards:
        oracle_only += 1
    if 'Thassa\'s Oracle' in cards and 'Underworld Breach' in cards:
        both += 1
    elif 'Thassa\'s Oracle' in cards or 'Underworld Breach' in cards:
        either += 1
    
    total += 1

print('Total decks in DDB (competitive and brewers corner):', total)
print('Decks with either:', either)
print('Decks with both:', both)
print('Decks with only Thoracle:', oracle_only)
print('Decks with only Breach:', breach_only)