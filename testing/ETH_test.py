import math
import json
import time
from datetime import datetime
from binance.client import Client

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

symbol = 'ETHBUSD'
time_to_cool_down = 5400
multiplier = 1.3

info = client.futures_exchange_info()


def get_precision(pair):
    for x in info['symbols']:
        if x['symbol'] == pair:
            return x['quantityPrecision']


def get_notional(pair):
    for x in info['symbols']:
        if x['symbol'] == pair:
            for y in x['filters']:
                if y['filterType'] == 'MIN_NOTIONAL':
                    return y['notional']


def round_up(n, decimals=0):
    round_up_multiplier = 10 ** decimals
    return math.ceil(n * round_up_multiplier) / round_up_multiplier


quantityPrecision = get_precision(symbol)
minNotional = round_up(float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
                       get_precision(symbol))

timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")
quantity = round(minNotional * multiplier, quantityPrecision)

client.futures_create_order(symbol=symbol,
                            quantity=quantity,
                            side='BUY',
                            positionSide='LONG',
                            type='MARKET')

client.futures_create_order(symbol=symbol,
                            quantity=quantity,
                            side='SELL',
                            positionSide='SHORT',
                            type='MARKET')

print(timestamp, symbol, 'long and short, wait', time_to_cool_down)