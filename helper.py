import re, math, secrets, argparse, functools, time

from binance.client import Client
from binance.helpers import round_step_size

parser = argparse.ArgumentParser()
parser.add_argument('--function', type=str, required=True)

client = Client("",
                "")

asset = "USDT"
# default = 6; min_notional can be extended #
min_notional = 10
# default = 1.2; min_notional_corrector needs to correct error of not creating close orders #
min_notional_corrector = 1.2

# amount of greed to add every time new trade is placed #
percentage_increase_of_base_greed = 0.02
# max greed be increased times #
times_base_greed_can_be_increased = 3

# without fee deduction #
base_percentage_futures_close = 0.999
percentage_futures_open = 1.25

# last digit is for hours to cooldown isMarketBuy, 1 - hour ago, 0.16 - 10 minutes ago #
newest_edge = 1000 * 60 * 60 * 0.5
# cooldown will be reset after relative_hours. Last digit is for hours  #
oldest_edge = 1000 * 60 * 60 * 1
# new short order will be opened after to_the_moon_cooldown. Last digit is for hours  #
to_the_moon_cooldown = 1000 * 60 * 60 * 48
# new short order will be canceled only after cooldown_to_cancel_order_without_position. Last digit is for hours  #
cooldown_to_cancel_order_without_position = 1000 * 60 * 60 * 1

# last digit is for days #
deltaTime = 1000 * 60 * 60 * 24 * 14
# most likely, it will not fall less than 0.79, so lower limit orders will be cancelled after deltaTime #
percentage_spot_open = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]

symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']
availableBalance = round(float(client.futures_account()["availableBalance"]))


def timeit(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsed_time * 1_000)))
        return result

    return new_func


@timeit
def set_futures_change_leverage():
    for x in client.futures_ticker():
        try:
            print(client.futures_change_leverage(symbol=x["symbol"], leverage=1))
        except Exception:
            print("fail to set_futures_change_leverage of", x["symbol"])


@timeit
def set_futures_change_multi_assets_mode():
    try:
        client.futures_change_multi_assets_mode(multiAssetsMargin="True")
    except Exception:
        print("fail to set_futures_change_multi_assets_mode")


@timeit
def get_notional(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'MIN_NOTIONAL':
                        return y['notional']
    except Exception:
        print("fail to get_notional of", symbol)


@timeit
def get_tick_size(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'PRICE_FILTER':
                        return y['tickSize']
    except Exception:
        print("fail to get_tick_size of", symbol)


@timeit
def get_step_size(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'MARKET_LOT_SIZE':
                        return y['stepSize']
    except Exception:
        print("fail to get_step_size of", symbol)


@timeit
def get_quantity_precision(symbol):
    try:
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                return x["quantityPrecision"]
    except Exception:
        print("fail to get_quantity_precision of", symbol)


@timeit
def get_quantity(symbol):
    try:
        quantity = round(
            (float(get_notional(symbol)) * set_greed())
            / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
            get_quantity_precision(symbol)
        )

    except Exception:
        print("fail to get_quantity of", symbol)
    return quantity


@timeit
def get_futures_tickers_to_short():
    # exclude balance_asset tickers #
    futures_account_balance_asset = []
    for x in client.futures_account_balance():
        futures_account_balance_asset.append(x["asset"] + asset)

    # exclude BUSD and quarterly tickers #
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

    # exclude tickers with onboardDate < deltaTime #
    onboardDate = []
    for x in client.futures_exchange_info()["symbols"]:
        if float(x["onboardDate"]) > serverTime - deltaTime:
            onboardDate.append(x["symbol"])

    tickers_after_excluding = set(all_tickers) - set(exist_positions) - set(futures_account_balance_asset) - set(
        onboardDate) - set(fundingRate) - set(get_open_orders_without_position())

    return list(tickers_after_excluding)


@timeit
def set_greed():
    try:
        # set base_greed #
        base_greed = math.ceil(((float(client.futures_account()['totalWalletBalance']) * min_notional_corrector) / (
                len(client.futures_ticker()) * min_notional)))
        print("base_greed", base_greed)

        # get greed of last trade relative base_greed #
        income_and_time = {"income": [], "time": []}

        for x in client.futures_income_history():
            if x["incomeType"] == "REALIZED_PNL":
                income_and_time["income"].append(x["income"])
                income_and_time["time"].append(x["time"])

        income = income_and_time["income"][
            income_and_time["time"].index(
                max(income_and_time["time"]))]

        greed_of_last_trade = round(
            (float(income) / (1 - base_percentage_futures_close)) / float(
                get_notional("ETHUSDT")), 2)

        print("greed_of_last_trade", greed_of_last_trade)

        times_base_greed_can_be_increased_in_timeframe = 0
        # to increase or not based by last maker trade with realized_pnl #
        for x in client.futures_income_history():
            if x["incomeType"] == "REALIZED_PNL" and x["time"] > (serverTime - newest_edge):
                times_base_greed_can_be_increased_in_timeframe = times_base_greed_can_be_increased_in_timeframe + 1

        greed_for_new_trade = greed_of_last_trade + times_base_greed_can_be_increased_in_timeframe * percentage_increase_of_base_greed
        print(greed_for_new_trade)

    except Exception:
        print("fail to set_greed")

    return min(round(greed_for_new_trade, 2), round((base_greed * times_base_greed_can_be_increased), 2))


@timeit
def create_open_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[1]["markPrice"])
                                                          * percentage_futures_open, get_tick_size(symbol)),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception:
        print("fail to open limit for", symbol)


@timeit
def create_close_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(abs((float(
                                        client.futures_position_information(symbol=symbol)[1]["positionAmt"]))),
                                        get_step_size(symbol)),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[1]["entryPrice"])
                                                          * base_percentage_futures_close,
                                                          get_tick_size(symbol)),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception:
        print("fail to create LIMIT for", symbol)


@timeit
def close_exist_positions():
    try:
        for x in client.futures_position_information():
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
                    create_close_limit(symbol)

                if count_sell_orders == 0 and x["updateTime"] < serverTime - to_the_moon_cooldown:
                    create_open_limit(symbol)
    except Exception:
        print("fail to create close exist positions for", symbol)


@timeit
def cancel_close_order_if_filled():
    try:
        for x in client.futures_position_information():
            if float(x["positionAmt"]) < 0:
                symbol = x["symbol"]

                for x in client.futures_get_open_orders(symbol=symbol):
                    if x["side"] == "BUY" and abs(float(x["positionAmt"])) != float(x["origQty"]):
                        client.futures_cancel_order(symbol=symbol, orderId=x["orderId"])

    except Exception:
        print("fail to cancel close order if filled for", symbol)


@timeit
def get_open_orders_without_position():
    try:
        open_orders = []
        for x in client.futures_get_open_orders():
            open_orders.append(x["symbol"])

        positions = []
        for x in client.futures_position_information():
            if float(x["positionAmt"]) < 0:
                positions.append(x["symbol"])

    except Exception:
        print("fail to get open orders without position for", open_orders)

    return list(set(open_orders) - set(positions))


@timeit
def cancel_open_orders_without_position():
    try:

        for x in get_open_orders_without_position():
            if serverTime > float(client.futures_get_open_orders(symbol=x)[0][
                                      "updateTime"]) + cooldown_to_cancel_order_without_position:
                client.futures_cancel_all_open_orders(symbol=x)

    except Exception:
        print("fail to cancel open orders without position for", x)


@timeit
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


@timeit
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
                                   * secrets.choice(percentage_spot_open),
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


@timeit
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


@timeit
def get_futures_income_history():
    futures_income_history = []
    for x in client.futures_income_history():
        if x["incomeType"] == 'REALIZED_PNL':
            futures_income_history.append(x["time"])

    return max(futures_income_history)


# --function open_for_profit #
@timeit
def open_for_profit():
    last_realized_pnl_trade = get_futures_income_history()

    if last_realized_pnl_trade + newest_edge > serverTime or serverTime > last_realized_pnl_trade + oldest_edge:

        # random #
        # symbol = secrets.choice(get_futures_tickers_to_short())

        # priceChangePercent #
        symbol_and_priceChangePercent = {"symbol": [], "priceChangePercent": []}

        for symbol in get_futures_tickers_to_short():
            symbol_and_priceChangePercent["symbol"].append(client.futures_ticker(symbol=symbol)["symbol"])
            symbol_and_priceChangePercent["priceChangePercent"].append(
                float(client.futures_ticker(symbol=symbol)["priceChangePercent"]))

        symbol = symbol_and_priceChangePercent["symbol"][
            symbol_and_priceChangePercent["priceChangePercent"].index(
                max(symbol_and_priceChangePercent["priceChangePercent"]))]

        try:
            client.futures_create_order(symbol=symbol,
                                        quantity=get_quantity(symbol),
                                        price=round_step_size(
                                            float(client.futures_mark_price(symbol=symbol)["markPrice"])
                                            * 1.003,
                                            get_tick_size(symbol)),
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC")
        except Exception:
            print("fail open_for_profit")


# --function close_with_profit #
@timeit
def close_with_profit():
    cancel_close_order_if_filled()
    close_exist_positions()
    cancel_open_orders_without_position()


# --function transfer_profit #
@timeit
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
if parser.parse_args().function == "initialized":
    set_futures_change_multi_assets_mode()
    set_futures_change_leverage()
