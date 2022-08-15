from flask import Flask, render_template, request, send_file
import sys
sys.path.insert(0, '../projects/power_level')
sys.path.insert(0, '../projects/api')
import mtg_api
import powerlevel

app = Flask(__name__)

@app.route('/2')
def home():
    return render_template("graph.html")

@app.route('/')
def home2():
    return render_template("graph3.html")

@app.route('/power-level', methods=['POST'])
def power_level():
    data = request.json
    url = data['url']
    decklist = mtg_api.get_deck(url).get_decklist()
    level = powerlevel.rate(decklist)
    return level

@app.route('/<color>')
def color_image(color):
    return send_file('color_images/'+color, mimetype='image/png')