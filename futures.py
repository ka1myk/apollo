#TODO fix create grid short lower avg price with 1/x (deeper and more volume to buy)
#TODO create grid short upper avg price 1/x (upper and more volume to buy)

import json
import math
import secrets

from binance.client import Client
from binance.helpers import round_step_size

from telegram_exception_alerts import Alerter

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])

symbol = secrets.choice(variables['coin']) + variables['currency']
client.futures_change_leverage(symbol=symbol, leverage=1)
futures_limit_short_grid = variables['futures_limit_short_grid']


def get_symbol_info():
    return client.futures_exchange_info()


def get_fees():
    return float(client.get_trade_fee(symbol=symbol)[0]["makerCommission"]) + float(
        client.get_trade_fee(symbol=symbol)[0]["takerCommission"])


# why 13440?
# 7 * 40 * 4 * 12 = 13440$ for 12 month
# len(coins) * week budget in $ * weeks in month * amount of month continuous trade
def set_greed():
    if float(client.futures_account()['totalWalletBalance']) < variables['budget_for_greed_increase_in_currency']:
        greed = 1
    else:
        greed = round(
            float(client.futures_account()['totalWalletBalance']) / variables['budget_for_greed_increase_in_currency'])
    return int(greed)


def get_quantity_precision(symbol: str) -> int:
    for x in get_symbol_info()['symbols']:
        if x['symbol'] == symbol:
            return int(x['quantityPrecision'])


def get_notional(symbol: str) -> float:
    for x in get_symbol_info()['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'MIN_NOTIONAL':
                    return float(y['notional'])


def round_up(n, decimals=0):
    round_up_multiplier = 10 ** decimals
    return math.ceil(n * round_up_multiplier) / round_up_multiplier


def get_tick_size(symbol: str) -> float:
    for x in get_symbol_info()['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'PRICE_FILTER':
                    return float(y['tickSize'])


def get_rounded_price(symbol: str, price: float) -> float:
    return round_step_size(price, get_tick_size(symbol))


def min_notional(symbol: str) -> float:
    return round_up(
        float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
        get_quantity_precision(symbol))


def open_market():
    client.futures_create_order(symbol=symbol,
                                quantity=round(min_notional(symbol) * set_greed(),
                                               get_quantity_precision(symbol)),
                                side='SELL',
                                positionSide='SHORT',
                                type='MARKET')


def create_grid(short_position_amt, futures_limit_short_grid, short_take_profit_price):
    for x in futures_limit_short_grid:
        x = x - get_fees()
        client.futures_create_order(symbol=symbol,
                                    quantity=round(short_position_amt / len(futures_limit_short_grid),
                                                   get_quantity_precision(symbol)),
                                    price=get_rounded_price(symbol, short_take_profit_price * x),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )


def create_limit():
    client.futures_cancel_all_open_orders(symbol=symbol)

    short_position_amt = abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]))
    short_take_profit_price = get_rounded_price(symbol, float(
        client.futures_position_information(symbol=symbol)[2]["entryPrice"]))

    order_qty = round(min_notional(symbol), get_quantity_precision(symbol))
    amount_of_close_orders = short_position_amt / order_qty

    if amount_of_close_orders > len(futures_limit_short_grid):
        amount_of_close_orders = len(futures_limit_short_grid)

    for x in range(int(amount_of_close_orders)):
        create_grid(short_position_amt, futures_limit_short_grid[x], short_take_profit_price)


@tg_alert
def go_baby_futures():
#    open_market()
    create_limit()


go_baby_futures()
