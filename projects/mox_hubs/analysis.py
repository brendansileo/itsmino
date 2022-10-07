import json

with open('hub_relationships.json', 'r') as f:
    hub_relations = json.load(f)

with open('hub_counts.json', 'r') as f:
    hub_counts = json.load(f)

total = 677308

color_hubs = ['Sultai (BGU)', 'Selesnya (GW)', 'Bant (GWU)', 'Gruul (RG)', 'Naya (RGW)', 'Abzan (WBG)', 'Mono White', 'Orzhov (WB)', 'Temur (GUR)', 'Golgari (BG)', 'Simic (GU)', 'Grixis (UBR)', 'Esper (WUB)', 'Jeskai (URW)', 'Rakdos (BR)', 'Five Color (WUBRG)', 'Izzet (UR)', 'Mardu (RWB)', 'Mono Red', 'Artifice (WUBR)', 'Mono Blue', 'Boros (RW)', 'Azorius (WU) ', 'Chaos (UBRG)', 'Mono Black', 'Growth (WUBG)', 'Mono Green', 'Dimir (UB)', 'Jund (BRG)', 'Altruism (WURG)', 'Aggression (WBRG)']
strategy_hubs = ['Vehicles', 'Thieves', 'Historic', 'Defender', 'Rock', 'Vorthos', 'Formula X-1', 'Stoneblade', 'Modular', 'Delver', 'Miracles', 'Blue Moon', 'Maverick', 'Combo', 'Tokens', 'Tribal', 'Enchantments', 'Aggro', 'Midrange', 'Storm', 'Aristocrats', 'Reanimator', 'Stax', 'Affinity', 'Artifacts', 'Mill', 'Land Destruction', 'Voltron', 'Wheels', 'Dredge', 'Control', 'Super Friends', 'Pillowfort', 'Discard', 'Extra Combats', 'Tempo', 'Infect', 'Mutate', 'Toolbox', 'Spellslinger', 'Life Gain', 'Suicide', 'Blink / Flicker', 'Hatebears', 'Burn', 'Lands Matter', '+1/+1 Counters', 'Group Slug', 'Zoo', 'Snow', 'Goodstuff', 'Ramp', 'Farm', 'Turbo', 'Extra Turns', 'Clones', 'Battlecruiser', 'Eggs', 'Auras', 'Equipment', 'Modified', '-1/-1 Counters', 'Cycling', 'Morph', 'Chaos', 'Death & Taxes', 'Birthing Pod / Pod', 'Devotion', 'Colorless', 'Flying', 'Tron', 'Group Hug', 'Aikido']
other_hubs = ['Help Wanted', 'Primer', 'Competitive', 'Casual', 'Jank', 'Unmaintained', 'Budget', 'Help Wanted', 'Webcam Friendly', 'PlayEDH - Low', 'PlayEDH - Mid', 'PlayEDH - High', 'PlayEDH - Maximum', 'PlayEDH - Battlecruiser']

with open('hub_analysis/by_strategy.txt', 'w') as f:
    for hub, relations in hub_relations.items():
        if hub not in strategy_hubs:
            continue
        f.write('~~~~~'+hub+'~~~~~\n')
        relation_hubs = { your_key: relations[your_key] for your_key in color_hubs }
        relation_hubs = {k: v for k, v in reversed(sorted(relation_hubs.items(), key=lambda item: item[1]))}
        for hub2, count in relation_hubs.items():
            f.write('    '+hub2+': '+str(count)+'\n')

with open('hub_analysis/by_color.txt', 'w') as f:
    for hub, relations in hub_relations.items():
        if hub not in color_hubs:
            continue
        f.write('~~~~~'+hub+'~~~~~\n')
        relation_hubs = { your_key: relations[your_key] for your_key in strategy_hubs }
        relation_hubs = {k: v for k, v in reversed(sorted(relation_hubs.items(), key=lambda item: item[1]))}
        for hub2, count in relation_hubs.items():
            f.write('    '+hub2+': '+str(count)+'\n')

with open('hub_analysis/by_color_ratio.txt', 'w') as f:
    for hub, relations in hub_relations.items():
        if hub not in color_hubs:
            continue
        f.write('~~~~~'+hub+'~~~~~\n')
        relation_hubs = { your_key: relations[your_key] for your_key in strategy_hubs }
        relation_hubs = {k: v for k, v in reversed(sorted(relation_hubs.items(), key=lambda item: item[1]))}
        for hub2, count in relation_hubs.items():
            f.write('    '+hub2+': '+str(round(count/hub_counts[hub]*100, 2))+'%\n')

with open('hub_analysis/by_strategy_ratio.txt', 'w') as f:
    for hub, relations in hub_relations.items():
        if hub not in strategy_hubs:
            continue
        f.write('~~~~~'+hub+'~~~~~\n')
        relation_hubs = { your_key: relations[your_key] for your_key in color_hubs }
        relation_hubs = {k: v for k, v in reversed(sorted(relation_hubs.items(), key=lambda item: item[1]))}
        for hub2, count in relation_hubs.items():
            f.write('    '+hub2+': '+str(round(count/hub_counts[hub]*100, 2))+'%\n')
