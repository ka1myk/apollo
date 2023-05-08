import re
import time
import math
import json
import secrets
from binance.client import Client
from binance.helpers import round_step_size

# min_notional can be extended #
min_notional = 6
# min_notional_corrector need to correct error of not creating close orders #
min_notional_corrector = 1.5
# profit is 0.5% #
futures_limit_short_grid_close = [0.995]
# callbackRate can be from 0.1% to 5% #
callbackRate = 0.1
# 3 times 3%, 3 times 6% #
futures_limit_short_grid_open = [1.03, 1.06, 1.09, 1.15, 1.21, 1.27]
# 60 secs * 5 minutes #
max_secs_to_wait_before_new_position = 60 * 5
# last digit is for days to cancel not filled limit orders #
deltaTime = 1000 * 60 * 60 * 24 * 7
# most likely, it will not fall less than 0.79, so lower limit orders can be cancelled and moved to funding #
spot_grid = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]

client = Client("",
                "")

symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']


def futures_tickers_to_short():
    futures_account_balance_asset = []
    for x in client.futures_account_balance():
        matchObj = re.search("^((?!USD).)*$", x["asset"])

        if matchObj:
            futures_account_balance_asset.append(x["asset"] + "USDT")

    allAvailible = []
    for futures in client.futures_ticker():

        remove_quarterly_contract = re.search("^((?!_).)*$", futures["symbol"])
        remove_BUSD_contract = re.search("^.*USDT$", futures["symbol"])

        if remove_quarterly_contract and remove_BUSD_contract and budget_to_one_short(
                futures["symbol"]) <= min_notional:
            allAvailible.append(futures["symbol"])

    existPosition = []
    for z in client.futures_position_information():

        if float(z["positionAmt"]) < 0:
            existPosition.append(z["symbol"])

    shortReady = set(allAvailible) - set(existPosition) - set(futures_account_balance_asset)
    return list(shortReady)


def budget_to_increase_greed():
    with open('variables.json', 'r') as f:
        contracts = f.read()

    count_for_greed = json.loads(contracts)

    budget_to_increase_greed = len(count_for_greed) * len(futures_limit_short_grid_open) * min_notional

    return budget_to_increase_greed


def set_greed():
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
    quantity = round_step_size((float(get_notional(symbol)) * set_greed() * min_notional_corrector / float(
        client.futures_mark_price(symbol=symbol)["markPrice"])), get_lot_size(symbol))

    if float(quantity) < float(get_lot_size(symbol)):
        quantity = get_lot_size(symbol)

    return quantity


def budget_to_one_short(symbol):
    return round(float(get_quantity(symbol)) * float(client.futures_mark_price(symbol=symbol)["markPrice"]), 1)


budgetContract = round(len(futures_limit_short_grid_open) * set_greed() * min_notional_corrector * min_notional)
availableBalance = round(float(client.futures_account()["availableBalance"]))
