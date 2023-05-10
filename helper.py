import re
import time
import math
import secrets
from binance.client import Client
from binance.helpers import round_step_size

client = Client("",
                "")

# min_notional can be extended #
min_notional = 6
# min_notional_corrector need to correct error of not creating close orders #
min_notional_corrector = 1.2
# 60 secs * 2 minutes #
secs_to_wait = 60 * 2

# callbackRate can be from 0.1% to 5% #
callbackRate = [0.1, 0.2, 0.3, 0.4, 0.5]
# profit is 0.05%, 0.1%, 0.15%, 0.2% or 0.25% #
futures_profit_percentage = [0.995, 0.99, 0.985, 0.98, 0.975]
# 3 times 3%, 3 times 6% #
futures_limit_short_grid_open = [1.03, 1.06, 1.09, 1.15, 1.21, 1.27]

# last digit is for days to cancel not filled limit orders #
deltaTime = 1000 * 60 * 60 * 24 * 7
# most likely, it will not fall less than 0.79, so lower limit orders can be cancelled and moved to funding #
spot_grid = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]

symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']
availableBalance = round(float(client.futures_account()["availableBalance"]))


def get_futures_tickers_to_short():
    futures_account_balance_asset = []
    for x in client.futures_account_balance():
        futures_account_balance_asset.append(x["asset"] + "USDT")

    all_tickers = []
    for futures in client.futures_ticker():
        remove_quarterly_contract = re.search("^((?!_).)*$", futures["symbol"])
        remove_busd_contract = re.search("^.*USDT$", futures["symbol"])

        if remove_quarterly_contract and remove_busd_contract:
            all_tickers.append(futures["symbol"])

    exist_positions = []
    for z in client.futures_position_information():
        if float(z["positionAmt"]) < 0:
            exist_positions.append(z["symbol"])

    short_ready = set(all_tickers) - set(exist_positions) - set(futures_account_balance_asset)

    return list(short_ready)


def set_greed():
    budget_to_increase_greed = len(client.futures_ticker()) * len(futures_limit_short_grid_open) * min_notional
    greed = round(float(client.futures_account()['totalWalletBalance']) / budget_to_increase_greed, 1)

    if greed < 1:
        greed = 1

    return greed


def set_futures_change_leverage(symbol):
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


def get_step_size(symbol):
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            for y in x['filters']:
                if y['filterType'] == 'MARKET_LOT_SIZE':
                    return y['stepSize']


def get_quantity_precision(symbol):
    for x in symbol_info['symbols']:
        if x['symbol'] == symbol:
            return x["quantityPrecision"]


def get_quantity(symbol):
    quantity = round((float(get_notional(symbol)) * min_notional_corrector) / float(
        client.futures_mark_price(symbol=symbol)["markPrice"]), get_quantity_precision(symbol))

    return quantity


def get_usd_for_one_short(symbol):
    usd_for_one_short = round(
        float(get_quantity(symbol)) * float(client.futures_mark_price(symbol=symbol)["markPrice"]), 1)

    return usd_for_one_short


def get_usd_for_all_grid(symbol):
    usd_for_all_grid = round(len(futures_limit_short_grid_open) * set_greed() * get_usd_for_one_short(symbol))

    return usd_for_all_grid


def open_grid_limit(symbol):
    try:
        for x in futures_limit_short_grid_open:
            client.futures_create_order(symbol=symbol,
                                        quantity=get_quantity(symbol),
                                        price=round_step_size(float(
                                            client.futures_position_information(symbol=symbol)[2][
                                                "markPrice"]) * x, get_tick_size(symbol)),
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
    except:
        print("fail to open grid limit for", symbol)


def close_grid_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(abs((float(
                                        client.futures_position_information(symbol=symbol)[2][
                                            "positionAmt"]))), get_step_size(symbol)),
                                    activationPrice=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[2][
                                            "entryPrice"]) * secrets.choice(futures_profit_percentage),
                                                                    get_tick_size(symbol)),
                                    side='BUY',
                                    timeInForce="GTC",
                                    positionSide='SHORT',
                                    type='TRAILING_STOP_MARKET',
                                    callbackRate=secrets.choice(callbackRate)
                                    )
    except:
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(abs((float(
                                        client.futures_position_information(symbol=symbol)[2][
                                            "positionAmt"]))), get_step_size(symbol)),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[2][
                                            "entryPrice"]) * secrets.choice(futures_profit_percentage),
                                                          get_tick_size(symbol)),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
        print("fail to create TRAILING_STOP_MARKET, but create LIMIT for", symbol)


def close_exist_positions():
    try:
        for z in client.futures_position_information():
            if float(z["positionAmt"]) < 0:
                symbol = z["symbol"]

                count_buy_orders = 0
                count_sell_orders = 0

                for x in client.futures_get_open_orders(symbol=symbol):
                    if x["side"] == "BUY":
                        count_buy_orders = count_buy_orders + 1

                    if x["side"] == "SELL":
                        count_sell_orders = count_sell_orders + 1

                if count_buy_orders == 0:
                    close_grid_limit(symbol)

                if count_sell_orders == 0:
                    open_grid_limit(symbol)
    except:
        print("fail to create close exist positions for", symbol)


def cancel_close_order_if_filled():
    try:
        for z in client.futures_position_information():
            if float(z["positionAmt"]) < 0:
                symbol = z["symbol"]

                for x in client.futures_get_open_orders(symbol=symbol):
                    if x["side"] == "BUY":
                        if abs(float(z["positionAmt"])) != float(x["origQty"]):
                            client.futures_cancel_order(symbol=symbol, orderId=x["orderId"])

    except:
        print("fail to cancel close order if filled for", symbol)


def cancel_open_orders_without_position():
    try:
        open_orders = []
        positions = []

        for x in client.futures_get_open_orders():
            open_orders.append(x["symbol"])
        for y in client.futures_position_information():
            if float(y["positionAmt"]) < 0:
                positions.append(y["symbol"])

        for x in list(set(open_orders) - set(positions)):
            client.futures_cancel_all_open_orders(symbol=x)
    except:
        print("fail to cancel open orders without position for", open_orders)
