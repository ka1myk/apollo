#TODO calculate long_profit_percentage as average of timeframe change six month

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

info = client.get_symbol_info(symbol)
price = client.get_avg_price(symbol=symbol)['price']


def get_notional():
    for y in info['filters']:
        if y['filterType'] == 'MIN_NOTIONAL':
            return y['minNotional']


def get_price_precision(symbol):
    n = len(str(get_rounded_price(symbol, price)).split(".")[1])
    return n


def get_tick_size():
    for y in info['filters']:
        if y['filterType'] == 'PRICE_FILTER':
            return y['tickSize']


def get_rounded_price(symbol: str, price: float) -> float:
    return round_step_size(price, get_tick_size(symbol))


def open_market_and_create_close():
    client.order_market_buy(symbol=symbol, side='BUY', type='MARKET',
                            quoteOrderQty=float(get_notional(symbol)) * float(greed))

    avg_price_with_profit_and_precision = round(float(price) * float(long_profit_percentage),
                                                get_price_precision(symbol))
    executedQty = float(client.get_all_orders(symbol=symbol, limit=1)[0]["executedQty"])

    client.order_limit_sell(symbol=symbol, quantity=executedQty,
                            price=avg_price_with_profit_and_precision)


open_market_and_create_close()
