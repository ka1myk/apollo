import re
import time
import math
import json
import secrets
from binance.client import Client
from binance.helpers import round_step_size

# can be extended up to 10 #
min_notional = 10
# profit is 1% #
futures_limit_short_grid_close = [0.99]
# 3 times 3%, 3 times 6%, 3 times 12% #
futures_limit_short_grid_open = [1.03, 1.06, 1.09, 1.15, 1.21, 1.27, 1.39, 1.51, 1.63]
# 3180 is 53 minutes * 60 secs #
max_secs_to_wait_before_new_position = 3180
# last digit is for days to cancel not filled limit orders #
deltaTime = 1000 * 60 * 60 * 24 * 7
# most likely, it will not fall by less than 0.79, so lower limit orders can be cancelled and move to funding #
spot_grid = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73, 0.61, 0.49, 0.37]

client = Client("",
                "")

symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']


def futures_tickers_to_short():
    allAvailible = []
    for futures in client.futures_ticker():
        matchObj = re.search("^((?!_).)*$", futures["symbol"])
        if matchObj and budget_to_one_short(futures["symbol"]) <= min_notional:
            allAvailible.append(futures["symbol"])

    existPosition = []
    for z in client.futures_position_information():
        if float(z["positionAmt"]) < 0:
            existPosition.append(z["symbol"])

    shortReady = set(allAvailible) - set(existPosition)
    return list(shortReady)


def budget_to_increase_greed():
    contracts_amount = 0
    for futures in client.futures_ticker():
        contracts_amount = contracts_amount + 1
    budget_to_increase_greed = contracts_amount * len(futures_limit_short_grid_open) * min_notional

    return budget_to_increase_greed


def set_greed_and_min_notional_corrector():
    if float(client.futures_account()['totalWalletBalance']) < budget_to_increase_greed():
        greed = 1.2
    else:
        greed = round(float(client.futures_account()['totalWalletBalance']) / budget_to_increase_greed(), 1)

    return greed


def futures_change_leverage(symbol):
    client.futures_change_leverage(symbol=symbol, leverage=1)


def get_notional(symbol):
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'MIN_NOTIONAL':
                    return y['notional']


def get_tick_size(symbol):
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'PRICE_FILTER':
                    return y['tickSize']


def get_lot_size(symbol):
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'LOT_SIZE':
                    return y['stepSize']


def get_quantity(symbol):
    quantity = round_step_size((float(get_notional(symbol)) / float(
        client.futures_mark_price(symbol=symbol)[
            "markPrice"])) * set_greed_and_min_notional_corrector(), get_lot_size(symbol))

    if float(quantity) < float(get_lot_size(symbol)):
        quantity = get_lot_size(symbol)

    return quantity


def budget_to_one_short(symbol):
    return round(float(get_quantity(symbol)) * float(client.futures_mark_price(symbol=symbol)["markPrice"]), 1)


budgetContract = round(len(futures_limit_short_grid_open) * set_greed_and_min_notional_corrector() * min_notional)
availableBalance = round(float(client.futures_account()["availableBalance"]))
