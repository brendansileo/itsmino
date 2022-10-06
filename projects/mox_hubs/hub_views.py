import json

with open('hubs_deck_data.json', 'r') as f:
    data = json.load(f)

most_views = {}
for id, deck in data.items():
    views = deck['viewCount']
    for hub in deck['hubNames']:
        if hub not in most_views:
            most_views[hub] = {'deck': None, 'views': 0}
        if views > most_views[hub]['views']:
            most_views[hub] = {'deck': deck['publicUrl'], 'views': views}
most_views = {k: v for k, v in reversed(sorted(most_views.items(), key=lambda item: item[1]['views']))}
with open('hub_analysis/most_viewed.json', 'w') as f:
    f.write(json.dumps(most_views, indent=4))