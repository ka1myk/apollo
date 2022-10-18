import argparse
import json
import secrets

from binance.client import Client
from binance.helpers import round_step_size

with open('variables.json') as v:
    variables = json.load(v)

parser = argparse.ArgumentParser()

parser.add_argument('--pair', type=str, required=True)

args = vars(parser.parse_args())

symbol = args['pair']

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])

info = client.get_symbol_info(symbol)
price = client.get_avg_price(symbol=symbol)['price']

sell_profit = [1.005, 1.01, 1.015, 1.02, 1.025, 1.03, 1.035, 1.04, 1.045, 1.05]
buy_profit = [0.995, 0.99, 0.985, 0.98, 0.975, 0.97, 0.965, 0.96, 0.955, 0.95]


def set_greed():
    if float(client.get_margin_account()['totalAssetOfBtc']) < 0.1:
        greed = 1
    else:
        greed = round(float(client.get_margin_account()['totalAssetOfBtc']) / 0.1)
    return int(greed)


def get_min_notional():
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


# multiplication by 2 is crutching
def get_quote_order_qty() -> float:
    return float(get_min_notional()) * set_greed() * 2


def margin_create_market_buy():
    client.create_margin_order(symbol=symbol,
                               side='BUY',
                               type='MARKET',
                               quoteOrderQty=get_quote_order_qty())


def margin_create_market_sell():
    client.create_margin_order(symbol=symbol,
                               side='SELL',
                               type='MARKET',
                               quoteOrderQty=get_quote_order_qty())


def margin_create_limit_sell():
    avg_price_with_sell_profit_and_precision = round(
        float(price) * float(secrets.choice(sell_profit)),
        get_price_precision(symbol))

    quantity = float(client.get_all_margin_orders(symbol=symbol, limit=1)[0]["origQty"])
    client.create_margin_order(symbol=symbol, side='SELL', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_sell_profit_and_precision)


def margin_create_limit_buy():
    avg_price_with_buy_profit_and_precision = round(
        float(price) * float(secrets.choice(buy_profit)),
        get_price_precision(symbol))

    quantity = float(client.get_all_margin_orders(symbol=symbol, limit=1)[0]["origQty"])
    client.create_margin_order(symbol=symbol, side='BUY', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_buy_profit_and_precision)


if secrets.randbelow(2) == 1:
    margin_create_market_buy()
    margin_create_limit_sell()
else:
    margin_create_market_sell()
    margin_create_limit_buy()
