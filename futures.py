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
times_a_week_futures = variables['coin'][coin.coin]['times_a_week_futures']

client.futures_change_leverage(symbol=symbol, leverage=2)

info = client.futures_exchange_info()


# why 3360?
# 7 * 40 * 4 * 3 = 3360$ for 3 month
# len(coins) * week budget in $ * weeks in month * amount of month continuous trade
def set_greed():
    if float(client.futures_account()['totalWalletBalance']) < 3360:
        greed = 1
    else:
        greed = round(float(client.futures_account()['totalWalletBalance']) / 3360)
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


def open_market():
    client.futures_create_order(symbol=symbol,
                                quantity=round(min_notional(symbol) * multiplier_of_twice_BTC(symbol) * set_greed(),
                                               get_quantity_precision(symbol)),
                                side='SELL',
                                positionSide='SHORT',
                                type='MARKET')


def create_limit():
    order_qty = round(min_notional(symbol) * multiplier_of_twice_BTC(symbol), get_quantity_precision(symbol))
    amount_of_close_orders = short_position_amt / (order_qty * times_a_week_futures)

    client.futures_cancel_all_open_orders(symbol=symbol)

    if amount_of_close_orders <= 1:
        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 1,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.97),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

    if 1 < amount_of_close_orders <= 2:
        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 2,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.94),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 2,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.88),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

    if 2 < amount_of_close_orders <= 3:
        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 3,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.85),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 3,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.82),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 3,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.79),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

    if amount_of_close_orders > 3:
        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 4,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.76),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 4,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.73),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 4,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.70),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )

        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / 4,
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * 0.67),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )


open_market()
create_limit()