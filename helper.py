# TODO additional ip to ubuntu to run few instance
# TODO add send profit from another - instance print(client.get_deposit_address(coin='USDT'))
# TODO add parse keys from external
# TODO sum funding rate to profit
# TODO futuresboard refactor

import re, math, secrets, argparse
from binance.client import Client
from binance.helpers import round_step_size

parser = argparse.ArgumentParser()
parser.add_argument('--function', type=str, required=True)

client = Client("",
                "")

asset = "USDT"
# default = 6; min_notional can be extended #
min_notional = 50
# default = 1.2; min_notional_corrector needs to correct error of not creating close orders #
min_notional_corrector = 8
# 1m, 3m, 5m, 15m (+), 30m (+), 1h (+), 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M #
klines_interval = "15m"
futures_close_profit = [0.995]
futures_open_short = [1.10]
# last digit is for days to cancel not filled limit orders #
deltaTime = 1000 * 60 * 60 * 24 * 7
# last digit is for hours to cooldown isMarketBuy #
last_isBuyerMaker_time = 1000 * 60 * 60 * 1
# hours after cooldown is reseted #
relative_hours = 6
# most likely, it will not fall less than 0.79, so lower limit orders can be cancelled and moved to funding #
spot_open_long = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]

symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']
availableBalance = round(float(client.futures_account()["availableBalance"]))


def set_futures_change_leverage(symbol):
    client.futures_change_leverage(symbol=symbol, leverage=1)


def set_futures_change_multi_assets_mode():
    client.futures_change_multi_assets_mode(multiAssetsMargin="True")


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


def get_futures_tickers_to_short():
    # exclude balance_asset tickers #
    futures_account_balance_asset = []
    for x in client.futures_account_balance():
        futures_account_balance_asset.append(x["asset"] + asset)

    # exclude exist_positions tickers #
    all_tickers = []
    for x in client.futures_ticker():
        remove_quarterly_contract = re.search('^((?!_).)*$', x["symbol"])
        remove_busd_contract = re.search('^.*USDT$', x["symbol"])
        if remove_quarterly_contract and remove_busd_contract:
            all_tickers.append(x["symbol"])

    # exclude exist_positions tickers #
    exist_positions = []
    for x in client.futures_position_information():
        if float(x["positionAmt"]) < 0:
            exist_positions.append(x["symbol"])

    # exclude negative fundingRate tickers #
    fundingRate = []
    for x in client.futures_funding_rate():
        if float(x["fundingRate"]) < 0:
            fundingRate.append(x["symbol"])

    short_ready = set(all_tickers) - set(exist_positions) - set(futures_account_balance_asset) - set(fundingRate)

    return list(short_ready)


def set_greed():
    return max(
        round(
            float(client.futures_account()['totalWalletBalance'])
            / (len(client.futures_ticker()
                   * len(futures_open_short)
                   * min_notional)), 1),
        1
    )


def get_quantity(symbol):
    return round(
        (float(get_notional(symbol)) * min_notional_corrector)
        / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
        get_quantity_precision(symbol)
    )


def get_usd_for_one_short(symbol):
    return round(
        float(get_quantity(symbol))
        * float(client.futures_mark_price(symbol=symbol)["markPrice"]),
        1
    )


def get_usd_for_all_grid(symbol):
    return round(
        len(futures_open_short)
        * set_greed()
        * get_usd_for_one_short(symbol)
    )


def open_grid_limit(symbol):
    try:
        for x in futures_open_short:
            client.futures_create_order(symbol=symbol,
                                        quantity=get_quantity(symbol),
                                        price=round_step_size(float(
                                            client.futures_position_information(symbol=symbol)[2]["markPrice"])
                                                              * x, get_tick_size(symbol)),
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
    except Exception:
        print("fail to open grid limit for", symbol)


def close_grid_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(abs((float(
                                        client.futures_position_information(symbol=symbol)[2]["positionAmt"]))),
                                        get_step_size(symbol)),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[2]["entryPrice"])
                                                          * secrets.choice(futures_close_profit),
                                                          get_tick_size(symbol)),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception:
        print("fail to create LIMIT for", symbol)


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
    except Exception:
        print("fail to create close exist positions for", symbol)


def cancel_close_order_if_filled():
    try:
        for z in client.futures_position_information():
            if float(z["positionAmt"]) < 0:
                symbol = z["symbol"]

                for x in client.futures_get_open_orders(symbol=symbol):
                    if x["side"] == "BUY" and abs(float(z["positionAmt"])) != float(x["origQty"]):
                        client.futures_cancel_order(symbol=symbol, orderId=x["orderId"])

    except Exception:
        print("fail to cancel close order if filled for", symbol)


def cancel_open_orders_without_position():
    try:
        open_orders = []
        for x in client.futures_get_open_orders():
            open_orders.append(x["symbol"])

        positions = []
        for x in client.futures_position_information():
            if float(x["positionAmt"]) < 0:
                positions.append(x["symbol"])

        for x in list(set(open_orders) - set(positions)):
            client.futures_cancel_all_open_orders(symbol=x)

    except Exception:
        print("fail to cancel open orders without position for", open_orders)


def transfer_free_USD_to_spot():
    try:
        for x in client.futures_account_balance():
            select_USD_asset = re.search('^((?!USD).)*$', x["asset"])
            if not select_USD_asset and float(x["withdrawAvailable"]) > 0:
                try:
                    client.futures_account_transfer(asset=x["asset"],
                                                    amount=float(x["withdrawAvailable"]),
                                                    type=2,
                                                    timestamp=serverTime)
                except Exception:
                    print("fail transfer", x["asset"], "to spot")
    except Exception:
        print("fail transfer_free_USD_to_spot")


def buy_coins_on_spot():
    symbol = "BTCUSDT"

    for x in client.get_open_orders(symbol=symbol):
        try:
            if x["time"] < serverTime - deltaTime:
                client.cancel_order(symbol=symbol, orderId=x["orderId"])
        except Exception:
            print("fail to cancel orders older (serverTime - deltaTime)")

    if 10 < float(client.get_asset_balance(asset=asset)['free']) < 20:
        try:
            client.create_order(symbol=symbol,
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=math.floor(float(client.get_asset_balance(asset=asset)['free'])))
        except Exception:
            print("fail to buy market BTC for", asset)

    if float(client.get_asset_balance(asset=asset)['free']) > 20:
        try:
            client.create_order(symbol=symbol,
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=math.floor(float(client.get_asset_balance(asset=asset)['free']) * 0.5))

            client.order_limit(symbol=symbol,
                               quantity=client.get_all_orders(symbol=symbol)[-1]["origQty"],
                               price=round_step_size(
                                   float(client.get_avg_price(symbol=symbol)['price'])
                                   * secrets.choice(spot_open_long),
                                   get_tick_size(symbol=symbol)),
                               side='BUY',
                               type='LIMIT',
                               timeInForce="GTC"
                               )

        except Exception:
            print("fail to buy limit BTC for", asset)

    try:
        client.transfer_dust(asset=asset)
    except Exception:
        print("fail to dust", asset, "to BNB")


def transfer_free_spot_coin_to_futures():
    try:
        for x in client.futures_account_balance():
            select_USD_asset = re.search('^((?!USD).)*$', x["asset"])
            if select_USD_asset and float(client.get_asset_balance(asset=x["asset"])["free"]) > 0:
                try:
                    client.futures_account_transfer(asset=x["asset"],
                                                    amount=float(client.get_asset_balance(asset=x["asset"])["free"]),
                                                    type=1,
                                                    timestamp=serverTime)
                except Exception:
                    print("fail transfer", x["asset"], "to futures")
    except Exception:
        print("fail transfer_free_spot_coin_to_futures")


##### --function open_for_profit #####
def open_for_profit():
    for x in client.futures_ticker():
        for x in client.futures_account_trades(symbol=x["symbol"]):
            if x["side"] == "BUY" and (
                    (x["time"] + last_isBuyerMaker_time) > serverTime or
                    (x["time"] + last_isBuyerMaker_time * relative_hours) < serverTime
            ):
                ####
                symbol_and_priceChangePercent = {"symbol": [], "priceChangePercent": []}
                for symbol in get_futures_tickers_to_short():
                    symbol_and_priceChangePercent["symbol"].append(symbol)
                    symbol_and_priceChangePercent["priceChangePercent"].append(
                        round(float(client.futures_klines(symbol=symbol, interval=klines_interval)[-1][2]) / float(
                            client.futures_klines(symbol=symbol, interval=klines_interval)[-1][3]), 3)
                    )

                symbol = symbol_and_priceChangePercent["symbol"][
                    symbol_and_priceChangePercent["priceChangePercent"].index(
                        max(symbol_and_priceChangePercent["priceChangePercent"]))]

                if get_usd_for_all_grid(symbol) <= availableBalance and get_usd_for_one_short(symbol) <= min_notional:
                    try:
                        set_futures_change_leverage(symbol)
                        client.futures_create_order(symbol=symbol,
                                                    quantity=get_quantity(symbol),
                                                    side='SELL',
                                                    positionSide='SHORT',
                                                    type='MARKET')
                    except Exception:
                        print("fail open_for_profit")
                ####

                break
        else:
            continue
        break


##### --function close_with_profit #####
def close_with_profit():
    cancel_close_order_if_filled()
    close_exist_positions()
    cancel_open_orders_without_position()


##### --function transfer_profit #####
def transfer_profit():
    transfer_free_USD_to_spot()
    buy_coins_on_spot()
    transfer_free_spot_coin_to_futures()


if parser.parse_args().function == "open":
    open_for_profit()
if parser.parse_args().function == "close":
    close_with_profit()
if parser.parse_args().function == "transfer":
    transfer_profit()
