import json

with open('hubs_deck_data.json', 'r') as f:
    data = json.load(f)

total = 677308

hub_relations = {}

hub_counts = {}

for id, deck in data.items():
    for hub in deck['hubNames']:
        if hub not in hub_counts:
            hub_counts[hub] = 0
        if hub not in hub_relations:
            hub_relations[hub] = {}
        hub_counts[hub] += 1
        for hub2 in deck['hubNames']:
            if hub != hub2:
                if hub2 not in hub_relations[hub]:
                    hub_relations[hub][hub2] = 0
                hub_relations[hub][hub2] += 1
with open('hub_relationships.json', 'w') as f:
    f.write(json.dumps(hub_relations, indent=4))
with open('hub_counts.json', 'w') as f:
    f.write(json.dumps(hub_counts, indent=4))
