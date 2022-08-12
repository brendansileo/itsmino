from flask import Flask, render_template, request
import sys
sys.path.insert(0, '../projects/power_level')
sys.path.insert(0, '../projects/api')
import mtg_api
import powerlevel

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/power-level', methods=['POST'])
def power_level():
    data = request.json
    url = data['url']
    decklist = mtg_api.get_deck(url).get_decklist()
    level = powerlevel.rate(decklist)
    return level