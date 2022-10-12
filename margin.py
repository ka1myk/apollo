from secrets import randbelow
import json
import argparse
from binance.client import Client
from binance.helpers import round_step_size

with open('variables.json') as v:
    variables = json.load(v)

parser = argparse.ArgumentParser()

parser.add_argument('--pair', type=str, required=True)
parser.add_argument('--strategy', type=str, required=True)

args = vars(parser.parse_args())

symbol = args['pair']
strategy = args['strategy']

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])

info = client.get_symbol_info(symbol)
price = client.get_avg_price(symbol=symbol)['price']


def set_greed():
    if float(client.get_margin_account()['totalAssetOfBtc']) < 0.1:
        greed = 1
    else:
        greed = round(float(client.get_margin_account()['totalAssetOfBtc']) / 0.1)
    return greed


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


def get_quoteOrderQty(symbol: str) -> float:
    return float(get_notional(symbol)) * set_greed()


def get_qty_precision(symbol):
    n = len(str(float(client.get_all_margin_orders(symbol=symbol, limit=1)[0]["origQty"])).split(".")[1])
    return n


def margin_create_market_buy():
    client.create_margin_order(symbol=symbol,
                               side='BUY',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


def margin_create_market_sell():
    client.create_margin_order(symbol=symbol,
                               side='SELL',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


def margin_create_limit_sell():
    avg_price_with_sell_profit_and_precision = round(float(price) * float(1.004),
                                                     get_price_precision(symbol))

    quantity = round(float(client.get_all_margin_orders(symbol=symbol, limit=1)[0]["origQty"]) * 1.1,
                     get_qty_precision(symbol))

    client.create_margin_order(symbol=symbol, side='SELL', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_sell_profit_and_precision)


def margin_create_limit_buy():
    avg_price_with_buy_profit_and_precision = round(float(price) * float(0.996),
                                                    get_price_precision(symbol))

    quantity = round(float(client.get_all_margin_orders(symbol=symbol, limit=1)[0]["origQty"]) * 1.1,
                     get_qty_precision(symbol))

    client.create_margin_order(symbol=symbol, side='BUY', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_buy_profit_and_precision)


if strategy == "random":
    if randbelow(2) == 1:
        margin_create_market_buy()
        margin_create_limit_sell()
    else:
        margin_create_market_sell()
        margin_create_limit_buy()