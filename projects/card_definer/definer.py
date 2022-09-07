from bdb import effective
import copy
from difflib import SequenceMatcher
import re
from word2number import w2n
import json
from templates import *

cost_templates = {
    '((\{t})+)': tap_symbol,
    '((\{[w|u|b|r|g|c|\d+]})+)': mana
}

templates = {
        'add (.* mana of any color|(\{[w|u|b|r|g|c|\d]\})+)': add_mana,
        'remove .*? .*? counters from .*': remove_counters,
        'put .*? .*? counters on .*': put_counters,
        'gain.*life': gain_life,
        'gain control .*': gain_control,
        'enters .*': enters,
        'search your library .*': search,
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


def triggered(text):
    split_text = text.split(',')
    trigger, effect = split_text[0].strip(), ','.join(split_text[1:]).strip()
    if 'when ' in trigger:
        trigger_groups = re.findall('(when) (.*?) (.*)', trigger)
    else:
        trigger_groups = re.findall('(whenever|if) (you|an opponent|a player|~ or another .*?) (.*)', trigger)
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
        if ':' in ability:
            parsed_abilities['activated'].append(activated(ability))
        elif 'whenever ' in ability or 'when ' in ability or 'if ' in ability:
            parsed_abilities['triggered'].append(triggered(ability))
        else:
            if 'Creature' in card_info['type_line']:
                parsed_abilities['static'].append(ability)
            else:
                parsed_abilities['general'].append(general(ability))
    return parsed_abilities