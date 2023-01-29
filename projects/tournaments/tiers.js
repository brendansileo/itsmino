const { Client } = require('pg');
const request = require('request');

function sortDictByValue(dict) {
    // Convert the object to an array of key-value pairs
    const dictArray = Object.entries(dict);
    
    // Sort the array by value
    dictArray.sort((a, b) => b[1] - a[1]);
    
    // Convert the array back to an object
    const sortedDict = {};
    for (const [key, value] of dictArray) {
        sortedDict[key] = value;
    }
    return sortedDict;
}

function generateTierlist(min_count, decks, top16s, avg_attendents, image, name) {
    decks = JSON.parse(JSON.stringify(decks))
    top16s = JSON.parse(JSON.stringify(top16s))
    avg_attendents = JSON.parse(JSON.stringify(avg_attendents))
    ratios = {}
    for (var commander in decks) {
        if(decks[commander] < min_count) {
        delete avg_attendents[commander] 
        }
        else{
            if(!(commander in top16s)) {
                ratios[commander] = 0
            }
            else {
                ratios[commander] = top16s[commander]/decks[commander] * 100
            }
        }
    }
    var counts = sortDictByValue(decks)
    var ratios = sortDictByValue(ratios)
    var tiers = {'100': [[]], '90': [[]], '80': [[]], '70': [[]], '60': [[]], '50': [[]], '40': [[]], '30': [[]], '20': [[]], '10': [[]], '0': [[]]}
    var tiers_count = {'100': 0, '90': 0, '80': 0, '70': 0, '60': 0, '50': 0, '40': 0, '30': 0, '20': 0, '10': 0, '0': 0}
    
    for (var commander in ratios) {
        for (var key in tiers) {
            i = parseInt(key)
            if(ratios[commander] >= i && ratios[commander] < (i + 9.999999999999999)) {
                if(tiers[key][tiers[key].length-1].length >= 10) {
                    tiers[key].push([])
                }
                tiers[key][tiers[key].length-1].push([commander, ratios[commander]])
                tiers_count[key] += 1
            }
        }
    }

    nodes = []
    edges = []
    i = 0
    for (var tier in tiers) {
        for (var l in tiers[tier]) {
            for (var x in tiers[tier][l]) {
                key = tiers[tier][l][x][0]
                nodes.push({'commander': key, 'attendents': avg_attendents[key], 'size': counts[key], 'tier': i, 'image': image[key]})
            }
        }
        i += 1
    }

    var max_tier_length = 0
    for (var tier in tiers) {
        for (var l in tiers[tier]) {
            if(tiers[tier][l].length > max_tier_length) {
                max_tier_length = tiers[tier][l].length
            }
        }
    }   
    for (var i=0;i<max_tier_length;i++) {
        for (var tier in tiers) {
            for (var l in tiers[tier]) {
                for (var tier2 in tiers) {
                    for (var l2 in tiers[tier2]) {
                        if (tiers[tier][l] != tiers[tier2][l2]) {
                            try {
                                edges.push({'source': tiers[tier][l][i][0], 'dest': tiers[tier2][l2][i][0]})
                            }
                            catch(error) {}
                        }
                    }
                }
            }
        }
    }
    return [nodes, edges]
}



const client = new Client({
    user: 'pi',
    host: '24.62.6.16',
    database: 'cedh',
    password: 'password',
    port: 5432,
});

client.connect();

var decks = {}
var top16s = {}
var avg_attendents = {}
var image = {}

client.query('SELECT * FROM tiers', (err, res) => {
    for (var row in res['rows']) {
        commander = res['rows'][row]['commander']
        decks[commander] = res['rows'][row]['count']
        top16s[commander] = res['rows'][row]['top16s']
        avg_attendents[commander] = res['rows'][row]['attendents']
        image[commander] = res['rows'][row]['image']
    }
    all_nodes = {}
    all_edges = {}
    play_counts = Array.from(new Set(Object.values(decks)))
    for (var i in play_counts) {
        data = generateTierlist(play_counts[i], decks, top16s, avg_attendents, image, 'graph_'+i+'.html')
        all_nodes[play_counts[i].toString()] = data[0]
        all_edges[play_counts[i].toString()] = data[1]
    }

    client.end()
});