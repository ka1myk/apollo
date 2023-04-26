from helper import *

with open('variables.json', 'w') as f:
    json.dump(futures_tickers_to_short(), f)