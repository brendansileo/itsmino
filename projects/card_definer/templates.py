import re

def add_mana(text):
    data = {'action': 'add mana', 'details': {}}
    matches = re.search('add (.*)', text)
    data['details']['type'] = matches.group(1)
    return data

def tap_symbol(text):
    data = {'action': 'tap_symbol', 'details': {}}
    return data

def mana(text):
    data = {'action': 'mana', 'details': {}}
    colors = {'c': 'colorless', 'w': 'white', 'u':'blue', 'b': 'black', 'r': 'red', 'g': 'green', '\d+': 'generic'}
    for color, string in colors.items():
        for pip in re.findall(color, text):
            if string not in data['details']:
                    data['details'][string] = 0
            if string == 'generic':
                data['details'][string] += int(pip)
            else:
                data['details'][string] += 1
    return(data)

def remove_counters(text):
    data = {'action': 'remove counters', 'details': {}}
    split_text = text.split()
    data['details']['amount'] = w2n.word_to_num(split_text[1])
    data['details']['type'] = split_text[2]
    data['details']['from'] = re.findall('(?<=from) .*', text)[0].strip()
    return(data)

def put_counters(text):
    data = {'action': 'put counters', 'details': {}}
    split_text = text.split()
    data['details']['amount'] = w2n.word_to_num(split_text[1])
    data['details']['type'] = split_text[2]
    data['details']['on'] = re.findall('(?<=on) .*', text)[0].strip()
    return(data)

def gain_life(text):
    data = {'action': 'gain life', 'details': {}}
    amount = re.findall('(gain)(.*)(life)', text)
    if len(amount[0]) == 3 and amount[0][1] != ' ':
        data['details']['amount'] = amount[0][1]
    else:
        data['details']['type'] = 'trigger'
    return data

def gain_control(text):
    data = {'action': 'gain control', 'details': {}}
    if 'until' in text:
        find = re.findall('(gain control of )(.*)( until )(.*)', text)
        data['details']['duration'] = find[0][3]
    elif 'as long as you control ~' in text:
        find = re.findall('(gain control of )(.*) for as long as you control ~', text)
        data['details']['duration'] = 'while ~ in play'
    else:
        find = re.findall('(gain control of ) (.*)', text)
        data['details']['duration'] = 'indefinite'
    data['details']['target'] = find[0][1]
    return data

def enters(text):
    data = {'action': 'enters zone', 'details': {}}
    data['details']['zone'] = re.findall('(enters )(.*)', text)[0][1]
    return data

def search(text):
    data = {'action': 'search', 'details': {}}
    matches = re.findall('search your library for (.*card[s]?), put (it|that card|them) (.*), .*', text)
    data['details']['target'] = matches[0][0]
    data['details']['location'] = matches[0][2]
    return data

def sacrifice(text):
    data = {'action': 'sacrifice', 'details': {}}
    matches = re.split('sacrifice[s]?', text)
    if matches[0].strip() != '':
        data['details']['who'] = matches[0].strip()
    else:
        data['details']['who'] = 'self'
    data['details']['what'] = matches[1].strip()
    return data

def tap(text):
    data = {'action': 'tap', 'details': {}}
    matches = re.findall('tap (.*)', text)
    data['details']['target'] = matches[0]
    return data

def damage(text):
    data = {'action': 'damage', 'details': {}}
    matches = re.findall('deals (.*) damage to (.*)', text)
    data['details']['amount'] = matches[0][0]
    data['details']['target'] = matches[0][1]
    return data

def return_to_hand(text):
    data = {'action': 'return to hand', 'details': {}}
    if ' from ' not in text and ' in ' not in text:
        matches = re.findall('return (.*) to .*', text)
        data['details']['target'] = matches[0]
    else:
        matches = re.findall('return (.*) (?:from|in)? (.*?) to .*', text)
        data['details']['target'] = matches[0][0]
        data['details']['in'] = matches[0][1]
    return data

def destroy(text):
    data = {'action': 'destroy', 'details': {}}
    matches = re.findall('destroy (.*)', text)
    data['details']['target'] = matches[0]
    return data

def exile(text):
    data = {'action': 'exile', 'details': {}}
    matches = re.findall('exile (.*)', text)
    data['details']['target'] = matches[0]
    return data