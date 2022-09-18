import math
import json
from binance.client import Client
from binance.helpers import round_step_size
import argparse

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

with open('variables.json', 'r') as f:
    data = f.read()

variables = json.loads(data)

parser = argparse.ArgumentParser()
parser.add_argument('--coin', type=str, required=True)
coin = parser.parse_args()

currency = variables['currency']
symbol = coin.coin + currency
multiplier = variables[coin.coin]['multiplier']
greed = variables['greed']
leverage = variables['leverage']
amount_of_close_orders = 1
short_profit_percentage = variables[coin.coin]['short_profit_percentage']
unRealizedProfit_multiplayer = variables[coin.coin]['unRealizedProfit_multiplayer']

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

if float(short_position_amt) != 0:
    if abs(float(client.futures_position_information(symbol=symbol)[2]["unRealizedProfit"])) > abs(
            float(variables[coin.coin][
                      "previous_unRealizedProfit"])) * unRealizedProfit_multiplayer:
        variables[coin.coin][
            "previous_unRealizedProfit"] = client.futures_position_information(symbol=symbol)[2]["unRealizedProfit"]
        variables[coin.coin]['multiplier'] = variables[coin.coin]['multiplier'] * 2

        with open('variables.json', 'w') as f:
            json.dump(variables, f)

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
                                        price=get_rounded_price(symbol, short_take_profit_price * (1 - 0.01 * i)),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
else:
    variables[coin.coin]["previous_unRealizedProfit"] = 0
    variables[coin.coin]['multiplier'] = 1

    with open('variables.json', 'w') as f:
        json.dump(variables, f)

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
                                    price=get_rounded_price(symbol, short_take_profit_price * (1 - 0.01 * i)),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
