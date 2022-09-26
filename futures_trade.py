#TODO calculate multiplier as 40$ a week with greed=1
#TODO calculate short_profit_percentage as average of timeframe change six month

import math
import json
import argparse
from binance.client import Client
from binance.helpers import round_step_size

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

with open('variables.json') as v:
    variables = json.load(v)

parser = argparse.ArgumentParser()
parser.add_argument('--coin', type=str, required=True)
coin = parser.parse_args()

currency = variables['currency']
symbol = coin.coin + currency
greed = variables['greed']
leverage = variables['leverage']
multiplier = variables[coin.coin]['multiplier']
amount_of_close_orders = variables['amount_of_close_orders']
long_profit_percentage = variables[coin.coin]['long_profit_percentage']
short_profit_percentage = variables[coin.coin]['short_profit_percentage']

info = client.futures_exchange_info()


def get_quantity_precision(symbol):
    for x in info['symbols']:
        if x['symbol'] == symbol:
            return x['quantityPrecision']


def get_notional(symbol):
    for x in info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'MIN_NOTIONAL':
                    return y['notional']


def round_up(n, decimals=0):
    round_up_multiplier = 10 ** decimals
    return math.ceil(n * round_up_multiplier) / round_up_multiplier


def get_tick_size(symbol: str) -> float:
    for symbol_info in info['symbols']:
        if symbol_info['symbol'] == symbol:
            for symbol_filter in symbol_info['filters']:
                if symbol_filter['filterType'] == 'PRICE_FILTER':
                    return float(symbol_filter['tickSize'])


def get_rounded_price(symbol: str, price: float) -> float:
    return round_step_size(price, get_tick_size(symbol))


min_notional = round_up(
    float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
    get_quantity_precision(symbol))

short_position_amt = abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]))
short_take_profit_price = get_rounded_price(symbol, float(
    client.futures_position_information(symbol=symbol)[2]["entryPrice"]) * short_profit_percentage)


def open_market_and_create_close():
    client.futures_create_order(symbol=symbol,
                                quantity=round(min_notional * multiplier * greed, get_quantity_precision(symbol)),
                                side='SELL',
                                positionSide='SHORT',
                                type='MARKET')

    client.futures_cancel_all_open_orders(symbol=symbol)

    for i in range(amount_of_close_orders):
        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / amount_of_close_orders,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * (1 - 0.01 * (2 ** i))),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )


open_market_and_create_close()
