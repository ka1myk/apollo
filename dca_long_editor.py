from binance.client import Client
import time
import json

modifier = 2
max_wallet_exposure_limit = 2
delta_time = 87000  # 87000 is 24 hours. From epochconverter.com

client = Client('api',
                'secret')

def current_milli_time():
    return round(time.time() * 1000)

if ((client.futures_get_open_orders()[0]['time'] - current_milli_time()) > delta_time):

    with open('long.json') as f:
        data = json.load(f)

    if (data['long']['wallet_exposure_limit'] * modifier) < max_wallet_exposure_limit:
        data['long']['wallet_exposure_limit'] = float(data['long']['wallet_exposure_limit']) * modifier

        with open('long.json', 'w') as outfile:
            json.dump(data, outfile)
