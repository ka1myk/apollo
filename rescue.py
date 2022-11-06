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


def get_long_symbol():
    symbol = []
    for x in client.futures_account()["positions"]:
        if x["positionSide"] == "LONG" and float(x["entryPrice"]) > 0:
            symbol.append(x["symbol"])

    return symbol


symbol = secrets.choice(get_long_symbol())


def get_symbol_info():
    return client.futures_exchange_info()


def get_fees():
    return float(client.get_trade_fee(symbol=symbol)[0]["makerCommission"]) + float(
        client.get_trade_fee(symbol=symbol)[0]["takerCommission"])


# why 13440?
# 7 * 40 * 4 * 12 = 13440$ for 12 month
# len(coins) * week budget in $ * weeks in month * amount of month continuous trade
def set_greed():
    if float(client.futures_account()['totalWalletBalance']) < 13440:
        greed = 1
    else:
        greed = round(float(client.futures_account()['totalWalletBalance']) / 13440)
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
                                side='BUY',
                                positionSide='LONG',
                                type='MARKET')


def create_limit():
    client.futures_cancel_all_open_orders(symbol=symbol)

    long_position_amt = abs(float(client.futures_position_information(symbol=symbol)[1]["positionAmt"]))
    long_take_profit_price = get_rounded_price(symbol, float(
        client.futures_position_information(symbol=symbol)[1]["entryPrice"]))

    client.futures_create_order(symbol=symbol,
                                quantity=round(long_position_amt,
                                               get_quantity_precision(symbol)),
                                price=get_rounded_price(symbol, long_take_profit_price * 1.005),
                                side='SELL',
                                positionSide='LONG',
                                type='LIMIT',
                                timeInForce="GTC"
                                )


@tg_alert
def go_baby_rescue():
    long_position_amt = abs(float(client.futures_position_information(symbol=symbol)[1]["positionAmt"]))
    if long_position_amt > 0:
        open_market()
        create_limit()


go_baby_rescue()
