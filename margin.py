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


def margin_create_buy():
    client.create_margin_order(symbol=symbol,
                               side='BUY',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


def margin_create_sell():
    client.create_margin_order(symbol=symbol,
                               side='SELL',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


# margin_create_buy()
# margin_create_sell()

if strategy == "random":
    print(1)

if strategy == "liquidation":
    print(2)

if strategy == "tradingview":
    print(3)

if strategy == "rsi":
    print(4)

if strategy == "ma":
    print(5)

if strategy == "bollinger":
    print(6)

if strategy == "elliott":
    print(7)

if strategy == "volume":
    print(8)
