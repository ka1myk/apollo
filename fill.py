from helper import *

with open('variables.json', 'r') as f:
    data = f.read()

d = json.loads(data)
d = futures_tickers_to_short()

with open('variables.json', 'w') as f:
    json.dump(d, f)
