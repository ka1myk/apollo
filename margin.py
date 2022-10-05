# TODO profit percentage as variable
# TODO quantity: why * 1.01 and round to 4?
# TODO Proof-of-Concept

import json
import argparse
from binance.client import Client
from binance.helpers import round_step_size

with open('variables.json') as v:
    variables = json.load(v)

parser = argparse.ArgumentParser()
parser.add_argument('--pair', type=str, required=True)
pair = parser.parse_args()

symbol = pair.pair

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])

info = client.get_symbol_info(symbol)
price = client.get_avg_price(symbol=symbol)['price']


def get_notional(symbol):
    for y in info['filters']:
        if y['filterType'] == 'MIN_NOTIONAL':
            return y['minNotional']


def get_price_precision(symbol):
    n = len(str(get_rounded_price(symbol, price)).split(".")[1])
    return n


def get_tick_size(symbol):
    for y in info['filters']:
        if y['filterType'] == 'PRICE_FILTER':
            return y['tickSize']


def get_rounded_price(symbol: str, price: float) -> float:
    return round_step_size(price, get_tick_size(symbol))


def margin_create_sell_and_buy():
    avg_price_with_sell_profit_and_precision = round(float(price) * float(1.003),
                                                     get_price_precision(symbol))

    avg_price_with_buy_profit_and_precision = round(float(price) * float(0.997),
                                                    get_price_precision(symbol))

    quantity = round(float(get_notional(symbol)) * 1.01 / float(price), 4)

    client.create_margin_order(symbol=symbol, side='SELL', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_sell_profit_and_precision)

    client.create_margin_order(symbol=symbol, side='BUY', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_buy_profit_and_precision)


margin_create_sell_and_buy()
