from binance.client import Client
import time
import json
from variables import modifier, max_wallet_exposure_limit, delta_time

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)

client = Client(creds['binance_01']['key'],creds['binance_01']['secret'])

def current_milli_time():
    return round(time.time() * 1000)

if ((client.futures_get_open_orders()[0]['time'] - current_milli_time()) > delta_time):

    with open('long.json') as f:
        data = json.load(f)

    if (data['long']['wallet_exposure_limit'] * modifier) < max_wallet_exposure_limit:
        data['long']['wallet_exposure_limit'] = float(data['long']['wallet_exposure_limit']) * modifier

        with open('long.json', 'w') as outfile:
            json.dump(data, outfile)
