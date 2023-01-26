import json
import itertools
import numpy as np
with open('ddb_lists.json', 'r') as f:
    data = json.load(f)

seeds = ['Ad Nauseam', 'Underworld Breach', 'Rule of Law', 'Protean Hulk', 'Birthing Pod']

counts = {}
commonalities = {}
for name, cards in data.items():
    for card in cards:
        if 'Land' in data[name][card]['card']['type_line']:
            continue
        if card not in commonalities:
            commonalities[card] = {}
            counts[card] = 0
        counts[card] += 1
        for card2 in cards:
            if 'Land' in data[name][card2]['card']['type_line']:
                continue
            if card != card2:
                if card2 not in commonalities[card]:
                    commonalities[card][card2] = 0
                commonalities[card][card2] += 1

commonality_ratios = {}
for card in commonalities:
    commonality_ratios[card] = {}
    for card2 in commonalities[card]:
        commonality_ratios[card][card2] = commonalities[card][card2] / counts[card2]

dual_commonalities = {}
for card in commonality_ratios:
    dual_commonalities[card] = {}
    for card2 in commonality_ratios[card]:
        dual_commonalities[card][card2] = commonality_ratios[card][card2] * commonality_ratios[card2][card]
    dual_commonalities[card] = {k: v for k, v in reversed(sorted(dual_commonalities[card].items(), key=lambda item: item[1]))}

upper = .25
filtered_commonalities = {}
for card in dual_commonalities:
    #if counts[card] < 5:
    #    continue
    tmp = {}
    for card2, value in dual_commonalities[card].items():
        if value > upper:
            tmp[card2] = value
    if tmp != {}:
        filtered_commonalities[card] = {k: v for k, v in reversed(sorted(tmp.items(), key=lambda item: item[1]))}

packages = {}
for card in filtered_commonalities:
    if card not in seeds:
        continue
    keep = True
    #for check_card in filtered_commonalities:
        #if card != check_card:
            #if card in filtered_commonalities[check_card]:
                #if len(filtered_commonalities[check_card]) > len(filtered_commonalities[card]):
                    #keep = False
                #elif len(filtered_commonalities[check_card]) == len(filtered_commonalities[card]):
                    #if sum(filtered_commonalities[card].values()) < sum(filtered_commonalities[check_card].values()):
                        #keep = False
    if keep:
        packages[card] = filtered_commonalities[card]
package_lists = []
for card, package in packages.items():
    l = list(package.keys())
    l.append(card)
    l.sort()
    if l not in package_lists:
        package_lists.append(l) 

with open('packages.json', 'w') as f:
    f.write(json.dumps(packages, indent=4))