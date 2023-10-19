import random, re, math, secrets, argparse
import time

from binance.client import Client
from binance.helpers import round_step_size

client = Client("",
                "")

futures_ticker = client.futures_ticker()
futures_account = client.futures_account()
symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']
futures_account_balance = client.futures_account_balance()
futures_position_information = client.futures_position_information()

asset = "USDT"
# default = 6; min_notional can be extended #
min_notional = 10
# default = 1.2; min_notional_corrector needs to correct error of not creating close orders #
min_notional_corrector = 1.2

# if you know - you can extend #
leverage = 2

# for short without fee deduction #
short_base_percentage_futures_close = 0.997
short_base_percentage_futures_open = 1.10

# for long without fee deduction#
long_base_percentage_futures_close = 1.003
long_base_percentage_futures_open = 0.90

# tickers in one deal #
quantity_at_a_time = round(len(futures_ticker) * 0.02)

# last digit is for days #
deltaTime = 1000 * 60 * 60 * 24 * 1

# most likely, it will not fall less than 0.79, so lower limit orders will be cancelled after deltaTime #
percentage_spot_open = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]


def set_futures_change_leverage():
    for x in futures_ticker:
        try:
            print(client.futures_change_leverage(symbol=x["symbol"], leverage=leverage))
        except Exception as e:
            print("fail to set_futures_change_leverage of", x["symbol"], e)


def set_futures_change_multi_assets_mode():
    try:
        print(client.futures_change_multi_assets_mode(multiAssetsMargin=True))
    except Exception as e:
        print("fail to set_futures_change_multi_assets_mode", e)


def get_notional(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'MIN_NOTIONAL':
                        return y['notional']
    except Exception as e:
        print("fail to get_notional for", symbol, e)


def get_tick_size(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'PRICE_FILTER':
                        return y['tickSize']
    except Exception as e:
        print("fail to get_tick_size for", symbol, e)


def get_step_size(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'MARKET_LOT_SIZE':
                        return y['stepSize']
    except Exception as e:
        print("fail to get_step_size for", symbol, e)


def get_quantity_precision(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                return x["quantityPrecision"]
    except Exception as e:
        print("fail to get_quantity_precision for", symbol, e)


def get_quantity(symbol):
    try:
        quantity = round(
            (float(get_notional(symbol)) * set_greed())
            / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
            get_quantity_precision(symbol)
        )

    except Exception as e:
        print("fail to get_quantity for", symbol, e)
    return quantity


def get_futures_tickers():
    # exclude BUSD and quarterly tickers #
    all_tickers = []
    for x in futures_ticker:
        remove_quarterly_contract = re.search('^((?!_).)*$', x["symbol"])
        remove_busd_contract = re.search('^.*USDT$', x["symbol"])
        if remove_quarterly_contract and remove_busd_contract:
            all_tickers.append(x["symbol"])

    # exclude balance_asset tickers #
    futures_account_balance_asset = []
    for x in futures_account_balance:
        futures_account_balance_asset.append(x["asset"] + asset)

    # exclude tickers with onboardDate < deltaTime #
    onboardDate = []
    for x in symbol_info["symbols"]:
        if float(x["onboardDate"]) > serverTime - (deltaTime * 14):
            onboardDate.append(x["symbol"])

    tickers_after_excluding = set(all_tickers) - set(futures_account_balance_asset) - set(onboardDate)

    return list(tickers_after_excluding)


def short_get_futures_tickers():
    # exclude short_exist_positions tickers #
    short_exist_positions = []
    for x in futures_position_information:
        if float(x["positionAmt"]) < 0:
            short_exist_positions.append(x["symbol"])

    short_tickers_after_excluding = set(get_futures_tickers) - set(short_exist_positions)

    return list(short_tickers_after_excluding)


def long_get_futures_tickers():
    # exclude long_exist_positions tickers #
    long_exist_positions = []
    for x in futures_position_information:
        if float(x["positionAmt"]) > 0:
            long_exist_positions.append(x["symbol"])

    long_tickers_after_excluding = set(get_futures_tickers) - set(long_exist_positions)

    return list(long_tickers_after_excluding)


get_futures_tickers = get_futures_tickers()
short_get_futures_tickers = short_get_futures_tickers()
long_get_futures_tickers = long_get_futures_tickers()


def set_greed():
    try:
        base_greed = math.ceil(((float(futures_account['totalWalletBalance']) * min_notional_corrector * leverage) / (
                len(futures_ticker) * min_notional)))

    except Exception as e:
        print("fail to set_greed", e)

    return base_greed


def transfer_free_USD_to_spot():
    try:
        for x in futures_account_balance:
            select_USD_asset = re.search('^((?!USD).)*$', x["asset"])
            if not select_USD_asset and float(x["withdrawAvailable"]) > 0:
                try:
                    client.futures_account_transfer(asset=x["asset"],
                                                    amount=float(x["withdrawAvailable"]),
                                                    type=2,
                                                    timestamp=serverTime)
                except Exception as e:
                    print("fail transfer", x["asset"], "to spot", e)
    except Exception as e:
        print("fail transfer_free_USD_to_spot", e)


def buy_coins_on_spot():
    symbol = "BTCUSDT"

    for x in client.get_open_orders(symbol=symbol):
        try:
            if x["time"] < serverTime - (deltaTime * 7):
                client.cancel_order(symbol=symbol, orderId=x["orderId"])
        except Exception as e:
            print("fail to cancel orders older (serverTime - deltaTime)", e)

    if 10 < float(client.get_asset_balance(asset=asset)['free']) < 20:
        try:
            client.create_order(symbol=symbol,
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=math.floor(float(client.get_asset_balance(asset=asset)['free'])))
        except Exception as e:
            print("fail to buy market BTC for", asset, e)

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
                                   * secrets.choice(percentage_spot_open),
                                   get_tick_size(symbol=symbol)),
                               side='BUY',
                               type='LIMIT',
                               timeInForce="GTC"
                               )

        except Exception as e:
            print("fail to buy limit BTC for", asset, e)

    try:
        client.transfer_dust(asset=asset)
    except Exception as e:
        print("fail to dust", asset, "to BNB", e)


def transfer_free_spot_coin_to_futures():
    try:
        for x in futures_account_balance:
            select_USD_asset = re.search('^((?!USD).)*$', x["asset"])
            if select_USD_asset and float(client.get_asset_balance(asset=x["asset"])["free"]) > 0:
                try:
                    client.futures_account_transfer(asset=x["asset"],
                                                    amount=float(client.get_asset_balance(asset=x["asset"])["free"]),
                                                    type=1,
                                                    timestamp=serverTime)
                except Exception as e:
                    print("fail transfer", x["asset"], "to futures", e)
    except Exception as e:
        print("fail transfer_free_spot_coin_to_futures", e)


def short_create_open_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[1]["markPrice"])
                                                          * short_base_percentage_futures_open,
                                                          get_tick_size(symbol)),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception as e:
        print("fail to short_create_open_limit", symbol, e)


def long_create_open_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[0]["markPrice"])
                                                          * long_base_percentage_futures_open,
                                                          get_tick_size(symbol)),
                                    side='BUY',
                                    positionSide='LONG',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception as e:
        print("fail to long_create_open_limit", symbol, e)


def short_create_close_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(abs((float(
                                        client.futures_position_information(symbol=symbol)[1]["positionAmt"]))),
                                        get_step_size(symbol)),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[1]["entryPrice"])
                                                          * short_base_percentage_futures_close,
                                                          get_tick_size(symbol)),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception as e:
        print("fail to short_create_close_limit for", symbol, e)


def long_create_close_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(abs((float(
                                        client.futures_position_information(symbol=symbol)[0]["positionAmt"]))),
                                        get_step_size(symbol)),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[0]["entryPrice"])
                                                          * long_base_percentage_futures_close,
                                                          get_tick_size(symbol)),
                                    side='SELL',
                                    positionSide='LONG',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception as e:
        print("fail to long_create_close_limit", symbol, e)


def cancel_close_order_if_filled():
    for x in futures_position_information:
        if float(x["positionAmt"]) < 0:
            symbol = x["symbol"]
            try:
                for y in client.futures_get_open_orders(symbol=symbol):
                    if y["side"] == "BUY" and abs(float(x["positionAmt"])) != float(y["origQty"]):
                        client.futures_cancel_order(symbol=symbol, orderId=y["orderId"])
            except Exception as e:
                print("fail to cancel_close_short_order_if_filled", symbol, e)

    for x in futures_position_information:
        if float(x["positionAmt"]) > 0:
            symbol = x["symbol"]
            try:
                for y in client.futures_get_open_orders(symbol=symbol):
                    if y["side"] == "SELL" and abs(float(x["positionAmt"])) != float(y["origQty"]):
                        client.futures_cancel_order(symbol=symbol, orderId=y["orderId"])

            except Exception as e:
                print("fail to cancel_close_long_order_if_filled", symbol, e)


def cancel_open_orders_without_position():
    short_exist_positions = []
    for x in futures_position_information:
        if float(x["positionAmt"]) < 0:
            short_exist_positions.append(x["symbol"])

    long_exist_positions = []
    for x in futures_position_information:
        if float(x["positionAmt"]) > 0:
            long_exist_positions.append(x["symbol"])

    for x in client.futures_get_open_orders():
        if x['symbol'] not in short_exist_positions and x['positionSide'] == "SHORT":
            try:
                client.futures_cancel_order(symbol=x["symbol"], orderId=x["orderId"])
            except Exception as e:
                print("fail to cancel_open_orders_short_exist_positions", x, e)

        if x['symbol'] not in long_exist_positions and x['positionSide'] == "LONG":
            try:
                client.futures_cancel_order(symbol=x["symbol"], orderId=x["orderId"])

            except Exception as e:
                print("fail to cancel_open_orders_long_exist_positions", x, e)


def close_exist_positions():
    try:
        for x in futures_position_information:
            if float(x["positionAmt"]) < 0:
                symbol = x["symbol"]

                count_buy_orders = 0
                count_sell_orders = 0

                for x in client.futures_get_open_orders(symbol=symbol):
                    if x["side"] == "BUY":
                        count_buy_orders = count_buy_orders + 1

                    if x["side"] == "SELL":
                        count_sell_orders = count_sell_orders + 1

                if count_buy_orders == 0:
                    short_create_close_limit(symbol)

                if count_sell_orders == 0 and x["updateTime"] < serverTime - deltaTime:
                    short_create_open_limit(symbol)

        for x in futures_position_information:
            if float(x["positionAmt"]) > 0:
                symbol = x["symbol"]

                count_buy_orders = 0
                count_sell_orders = 0

                for x in client.futures_get_open_orders(symbol=symbol):
                    if x["side"] == "BUY":
                        count_buy_orders = count_buy_orders + 1

                    if x["side"] == "SELL":
                        count_sell_orders = count_sell_orders + 1

                if count_sell_orders == 0:
                    long_create_close_limit(symbol)

                if count_buy_orders == 0 and x["updateTime"] < serverTime - deltaTime:
                    long_create_open_limit(symbol)
    except Exception as e:
        print("fail to close_exist_positions", symbol, e)


def market_long_and_limit_long(trade_symbol):
    client.futures_create_order(symbol=trade_symbol,
                                quantity=get_quantity(trade_symbol),
                                side='BUY',
                                positionSide='LONG',
                                type='MARKET'
                                )
    time.sleep(1)
    client.futures_create_order(symbol=trade_symbol,
                                quantity=round_step_size(abs((float(
                                    client.futures_position_information(symbol=trade_symbol)[0]["positionAmt"]))),
                                    get_step_size(trade_symbol)),
                                price=round_step_size(float(
                                    client.futures_position_information(symbol=trade_symbol)[0]["entryPrice"])
                                                      * long_base_percentage_futures_close,
                                                      get_tick_size(trade_symbol)),
                                side='SELL',
                                positionSide='LONG',
                                type='LIMIT',
                                timeInForce="GTC"
                                )


def market_short_and_limit_short(trade_symbol):
    client.futures_create_order(symbol=trade_symbol,
                                quantity=get_quantity(trade_symbol),
                                side='SELL',
                                positionSide='SHORT',
                                type='MARKET'
                                )
    time.sleep(1)
    client.futures_create_order(symbol=trade_symbol,
                                quantity=round_step_size(abs((float(
                                    client.futures_position_information(symbol=trade_symbol)[1]["positionAmt"]))),
                                    get_step_size(trade_symbol)),
                                price=round_step_size(float(
                                    client.futures_position_information(symbol=trade_symbol)[1]["entryPrice"])
                                                      * short_base_percentage_futures_close,
                                                      get_tick_size(trade_symbol)),
                                side='BUY',
                                positionSide='SHORT',
                                type='LIMIT',
                                timeInForce="GTC"
                                )


# --function transfer #

def transfer_and_collect():
    transfer_free_USD_to_spot()
    buy_coins_on_spot()
    transfer_free_spot_coin_to_futures()


# --function close #

def cancel_and_close():
    cancel_close_order_if_filled()
    cancel_open_orders_without_position()
    close_exist_positions()


# --function open #

def choice_and_open():
    for i in range(quantity_at_a_time):
        try:
            symbol = random.choice(long_get_futures_tickers)
            market_long_and_limit_long(symbol)
            long_get_futures_tickers.remove(symbol)

            symbol = random.choice(short_get_futures_tickers)
            market_short_and_limit_short(symbol)
            short_get_futures_tickers.remove(symbol)
        except Exception as e:
            print(e)


parser = argparse.ArgumentParser()
parser.add_argument('--function', type=str, required=True)

if parser.parse_args().function == "open":
    choice_and_open()
if parser.parse_args().function == "close":
    cancel_and_close()
if parser.parse_args().function == "transfer":
    transfer_and_collect()
if parser.parse_args().function == "initialized":
    set_futures_change_multi_assets_mode()
    set_futures_change_leverage()