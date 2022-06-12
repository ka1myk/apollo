import math
import json
import time
import requests
from datetime import datetime
from binance.client import Client

with open('/root/binance_strategies/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

symbol = 'BNBBUSD'
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

while True:
    try:
        timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        bnb_coinglass_liquidation_endpoint = variables['bnb_coinglass_liquidation_endpoint']

        exception_cool_down = variables['exception_cool_down']
        qty_coins_liquidation = variables['qty_coins_liquidation']
        time_to_cool_down = variables['time_to_cool_down']
        multiplier = variables['multiplier']
        quantity = round(minNotional * multiplier, quantityPrecision)

        headers = {'coinglassSecret': creds['coinglass']['coinglassSecret']}
        url = requests.get(bnb_coinglass_liquidation_endpoint, headers=headers)
        text = url.text
        data = json.loads(text)

        long_signal = float(data['data'][90]['buyVolUsd']) / float(
            client.futures_mark_price(symbol=symbol)["markPrice"])
        short_signal = float(data['data'][90]['sellVolUsd']) / float(
            client.futures_mark_price(symbol=symbol)["markPrice"])

        print(timestamp, symbol, "qty_coins_liquidation", qty_coins_liquidation, "long_signal", long_signal,
              "short_signal", short_signal)

        if long_signal > qty_coins_liquidation:
            client.futures_create_order(symbol=symbol,
                                        quantity=quantity,
                                        side='BUY',
                                        positionSide='LONG',
                                        type='MARKET')
            print(timestamp, long_signal, symbol, 'open long and wait', time_to_cool_down)
            time.sleep(time_to_cool_down)

        if short_signal > qty_coins_liquidation:
            client.futures_create_order(symbol=symbol,
                                        quantity=quantity,
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='MARKET')
            print(timestamp, short_signal, symbol, 'open short and wait', time_to_cool_down)
            time.sleep(time_to_cool_down)

    except Exception as e:
        print(timestamp, "Function errored out!", e)
        time.sleep(exception_cool_down)