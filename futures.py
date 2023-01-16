# TODO fix create grid short lower avg price with 1/x (deeper and more volume to buy)
# TODO create grid short upper avg price 1/x (upper and more volume to buy)

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
symbol_info = client.futures_exchange_info()
client.futures_change_leverage(symbol=symbol, leverage=1)


def get_notional():
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'MIN_NOTIONAL':
                    return y['notional']


def get_tick_size():
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'PRICE_FILTER':
                    return y['tickSize']


def get_lot_size():
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'LOT_SIZE':
                    return y['stepSize']


def get_fees():
    return float(client.get_trade_fee(symbol=symbol)[0]["makerCommission"]) + float(
        client.get_trade_fee(symbol=symbol)[0]["takerCommission"])


def set_greed():
    if float(client.futures_account()['totalWalletBalance']) < variables['budget_up_to_1_greed']:
        greed = 1
    else:
        greed = round(
            float(client.futures_account()['totalWalletBalance']) / variables['budget_up_to_1_greed'])
    return greed


def futures_create_market_short():
    client.futures_create_order(symbol=symbol,
                                quantity=round_step_size(get_notional() * set_greed(), get_lot_size()),
                                side='SELL',
                                positionSide='SHORT',
                                type='MARKET')


def futures_create_grid_limit_short_down(short_position_amt, futures_limit_short_grid, short_take_profit_price):
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


def futures_create_grid_limit_short_up():
    for x in variables['futures_limit_short_grid_up']:
        x = x - get_fees()
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(get_notional() * set_greed(), get_lot_size()),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[2]["entryPrice"]) * x,
                                                          get_tick_size()),
                                    side='SELL',
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
    futures_create_grid_limit_short_down()
    futures_create_grid_limit_short_up()


go_baby_futures()
