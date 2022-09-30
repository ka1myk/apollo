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

info = client.get_symbol_info(symbol)
price = client.get_avg_price(symbol=symbol)['price']


def set_greed():
    if float(client.get_asset_balance(asset='BUSD')['free']) < 3000:
        greed = 1
    else:
        greed = round(float(client.get_asset_balance(asset='BUSD')['free']) / 3000)
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


def open_market():
    client.order_market_buy(symbol=symbol, side='BUY', type='MARKET',
                            quoteOrderQty=float(get_notional(symbol)) * set_greed())


open_market()
