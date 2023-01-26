from flask import Flask, render_template, request, send_file, redirect
import sys
import json
import os
sys.path.insert(0, '../projects/api')
import mtg_api

app = Flask(__name__)

with open('ddb.json', 'r') as f:
    decks_data = json.load(f)

@app.route('/categories')
def categories():
    with open('categories.txt', 'r') as f:
        data = f.read()
    return data

@app.route('/decks')
def decks():
    with open('ddb_names.txt', 'r') as f:
        data = f.read()
    return data

@app.route('/decks/<name>')
def decks_name(name):
    return json.dumps(decks_data[name], indent=4)

@app.route('/map/<cutoff>')
def map_home(cutoff):
    return render_template('graphs/graph_'+str(cutoff)+'.html')

@app.route('/map')
def map():
    fs = os.listdir('templates/graphs')
    cutoffs = []
    for f in fs:
        cutoffs.append(int(f.split('_')[1].split('.')[0]))
    return render_template('tierlist.html', cutoffs=sorted(set(cutoffs)))

@app.route('/tokens')
def tokens():
    return render_template('tokens.html')

@app.route('/tokens/<id>')
def tokens_export(id):
    deck = mtg_api.get_deck('https://moxfield.com/decks/'+id)
    info = deck.get_deck()
    tokens = info['tokens']
    res = []
    for token in tokens:
        if token['isToken']:
            res.append('1 '+token['name']+' Token ['+token['set'].upper()[1:]+']')
    return '\n'.join(sorted(list(set(res))))
