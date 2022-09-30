# TODO calculate short_profit_percentage as average of timeframe change six month

import math
import json
import argparse
from binance.client import Client
from binance.helpers import round_step_size

with open('variables.json') as v:
    variables = json.load(v)

parser = argparse.ArgumentParser()
parser.add_argument('--coin', type=str, required=True)
coin = parser.parse_args()

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
symbol = coin.coin + variables['currency']
amount_of_close_orders = variables['amount_of_close_orders']
times_a_week_futures = variables['coin'][coin.coin]['times_a_week_futures']

client.futures_change_leverage(symbol=symbol, leverage=3)

info = client.futures_exchange_info()


def set_greed():
    if float(client.futures_account()['totalWalletBalance']) < 3000:
        greed = 1
    else:
        greed = round(float(client.futures_account()['totalWalletBalance']) / 3000)
    return greed


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


def min_notional(symbol: str) -> float:
    return round_up(
        float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
        get_quantity_precision(symbol))


def multiplier_of_twice_BTC(symbol: str) -> float:
    return round(
        (2 * (min_notional("BTCBUSD") * float(client.futures_mark_price(symbol="BTCBUSD")["markPrice"]))) / (
                min_notional(symbol) * float(
            client.futures_mark_price(symbol=symbol)["markPrice"])) / times_a_week_futures, 2)


short_position_amt = abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]))
short_take_profit_price = get_rounded_price(symbol, float(
    client.futures_position_information(symbol=symbol)[2]["entryPrice"]))


def open_market_and_create_close():
    client.futures_create_order(symbol=symbol,
                                quantity=round(min_notional(symbol) * multiplier_of_twice_BTC(symbol) * set_greed(),
                                               get_quantity_precision(symbol)),
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
