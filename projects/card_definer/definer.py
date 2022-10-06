from bdb import effective
import copy
from difflib import SequenceMatcher
import re
import json
from templates import *

cost_templates = {
    '((\{t})+)': tap_symbol,
    '((\{[w|u|b|r|g|c|\d+]})+)': mana
}

templates = {
        '(add (.* mana of any color|(\{[w|u|b|r|g|c|\d]\})+))': add_mana,
        'remove .*? .*? counters from .*': remove_counters,
        '(?:put|distribute) .*? .*? counters on .*(?!=onto the battlefield)': put_counters,
        'gain.*life': gain_life,
        'gain control .*': gain_control,
        'enters .*': enters,
        'search your library (?:(?!this way).).*': search,
        '.*sacrifice.*': sacrifice,
        'tap .*': tap,
        'deals .* damage to .*': damage,
        'return .* to .* hand': return_to_hand,
        'destroy .*': destroy,
        'exile .*': exile
        }

all_templates = {**templates, **cost_templates}

def activated(text):
    split_text = text.split(':')
    c, e = split_text[0].strip(), split_text[1].strip()
    costs = c.split(',')
    matched_costs = []
    for cost in costs:
        for matcher, tool in all_templates.items():
            matches = re.findall(matcher, cost)
            for match in matches:
                if type(match) == tuple:
                    match = match[0]
                if match != '':
                    matched_costs.append(tool(match))

    effects = e.split('.')
    matched_effects = []
    for effect in effects:
        if effect != '':
            for matcher, tool in templates.items():
                matches = re.search(matcher, effect)
                if matches:
                    match = matches.group(0)
                    if type(match) == tuple:
                        match = match[0]
                    if match != '':
                        matched_effects.append(tool(match))

    return {'cost': matched_costs, 'effect': matched_effects}

triggers = ['creature entering the battlefield.*', 'dies', 'blocks .*', 'deals .*?damage to .*', 'enters the battlefield', 'cast .*', 'attacks.*', 'is turned face.*', 'becomes blocked .*', 'gain life']

def triggered(text):
    split_text = text.split(',')
    trigger, effect = split_text[0].strip(), ','.join(split_text[1:]).strip()
    trigger_groups = None
    if 'when ' in trigger:
        trigger_groups = re.findall('(when) (.*) ('+'|'.join(triggers)+')', trigger)
    elif 'beginning' in trigger:
        trigger_groups = re.findall('(at the beginning of) (.*?) (.*)', trigger)
    elif 'if ' in trigger:
        if trigger[:2] != 'if':
            split = re.findall('(.*) (if .*)', trigger)
            trigger = split[0][1][:-1] + ' ' + split[0][0] + '.'
        trigger_groups = re.findall('(if) (.*) (would .*|was .*|control .*)', trigger)
    elif 'whenever' in trigger:
        trigger_groups = re.findall('(whenever) (.*) ('+'|'.join(triggers)+')', trigger)
    if not trigger_groups:
        return None
    matched_trigger = {'triggerer': trigger_groups[0][1], 'action': None}
    for matcher, tool in templates.items():
        matches = re.findall(matcher, trigger_groups[0][2])
        for match in matches:
            if type(match) == tuple:
                match = match[0]
            if match != '':
                matched_trigger['action'] = tool(match)

    split_effect = effect.split('.')
    matched_effect = []
    for effect in split_effect:
        for matcher, tool in templates.items():
            matches = re.findall(matcher, effect)
            for match in matches:
                if type(match) == tuple:
                    match = match[0]
                if match != '':
                    matched_effect.append(tool(match))

    return {'trigger': matched_trigger, 'effect': matched_effect}

def general(text):
    split_effect = text.split('.')
    matched_effect = []
    for effect in split_effect:
        for matcher, tool in templates.items():
            matches = re.findall(matcher, effect)
            for match in matches:
                if type(match) == tuple:
                    match = match[0]
                if match != '':
                    matched_effect.append(tool(match))

    return {'effect': matched_effect}

def define(card_name, card_info, text):
    text = text.replace(card_name, '~')
    abilities = text.split('\n')
    parsed_abilities = {'triggered': [], 'activated': [], 'static': [], 'general': []}
    for ability in abilities:
        ability = re.sub('.* — ', '', ability)
        if ':' in ability:
            parsed_abilities['activated'].append(activated(ability))
        elif 'gain "' in ability or 'gains "' in ability or 'have "' in ability:
            pass
        elif 'whenever ' in ability or 'when ' in ability or 'if ' in ability:
            parsed_abilities['triggered'].append(triggered(ability))
        else:
            if 'Creature' in card_info['types']:
                parsed_abilities['static'].append(ability)
            else:
                parsed_abilities['general'].append(general(ability))
    return parsed_abilities