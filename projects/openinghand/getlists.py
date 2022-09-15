import json

with open('ddb.json', 'r') as f:
    data = json.load(f)

with open('ddb_names.txt', 'w') as f:
    f.write('\n'.join(list(data.keys())))