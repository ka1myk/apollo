# backlog
# TODO additional ip to ubuntu to run few instances
# TODO add send profit from another instance - print(client.get_deposit_address(coin='USDT'))
# TODO add parse keys from external
# TODO analysis: 23.07.23 - STMXUSDT check funding rate in history, what goes wrong?
# TODO analysis: 23.07.23 - STMXUSDT binance increase frequency from every eight hours to every two
# TODO analysis: 23.07.23 - STMXUSDT check funding rate history
# TODO dev: funding penalties add to profit close limit
# in progress
# TODO futuresboard v2 install
# TODO add base percentage_futures_close
# TODO increase percentage_futures_close based on trade frequency (reset if > newest_edge)
# TODO max open position value based on totalWalletBalance/greed < 3
# TODO merge all branches to main/dev


import re, math, secrets, argparse
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
percentage_increase_of_base_greed = 0.01
# max greed be increased times #
times_base_greed_can_be_increased = 2

# https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data #
# [1] - Open, [2] - High, [3] - Low, [4] - Close, [5] - Volume #
last_futures_klines_param = 3
penult_futures_klines_param = 3

# 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M #
klines_interval = "5m"
base_percentage_futures_close = 0.998
percentage_futures_open = 1.25

# last digit is for hours to cooldown isMarketBuy, 1 - hour ago, 0.16 - 10 minutes ago #
newest_edge = 1000 * 60 * 60 * 0.16
# cooldown will be reseted after relative_hours. Last digit is for hours  #
oldest_edge = 1000 * 60 * 60 * 6
# new short order will be opened after to_the_moon_cooldown. Last digit is for hours  #
to_the_moon_cooldown = 1000 * 60 * 60 * 12

# last digit is for days to cancel not filled limit orders #
deltaTime = 1000 * 60 * 60 * 24 * 7
# most likely, it will not fall less than 0.79, so lower limit orders will be cancelled after deltaTime #
percentage_spot_open = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]

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
        fundingRate) - set(onboardDate)

    # klines_params #
    klines_1d = []
    klines_12h = []
    klines_8h = []
    klines_6h = []
    klines_4h = []
    klines_2h = []
    klines_1h = []
    klines_30m = []
    klines_15m = []
    klines_5m = []

    for symbol in tickers_after_excluding:

        if round(float(client.futures_klines(symbol=symbol, interval="1d")[-1][last_futures_klines_param]) / float(
                client.futures_klines(symbol=symbol, interval="1d")[-2][penult_futures_klines_param]), 3) < 1:
            klines_1d.append(symbol)

        if round(float(client.futures_klines(symbol=symbol, interval="12h")[-1][last_futures_klines_param]) / float(
                client.futures_klines(symbol=symbol, interval="12h")[-2][penult_futures_klines_param]), 3) < 1:
            klines_12h.append(symbol)

        # if round(float(client.futures_klines(symbol=symbol, interval="8h")[-1][last_futures_klines_param]) / float(
        #         client.futures_klines(symbol=symbol, interval="8h")[-2][penult_futures_klines_param]), 3) < 1:
        #     klines_8h.append(symbol)

        if round(float(client.futures_klines(symbol=symbol, interval="6h")[-1][last_futures_klines_param]) / float(
                client.futures_klines(symbol=symbol, interval="6h")[-2][penult_futures_klines_param]), 3) < 1:
            klines_6h.append(symbol)

        # if round(float(client.futures_klines(symbol=symbol, interval="4h")[-1][last_futures_klines_param]) / float(
        #         client.futures_klines(symbol=symbol, interval="4h")[-2][penult_futures_klines_param]), 3) < 1:
        #     klines_4h.append(symbol)

        # if round(float(client.futures_klines(symbol=symbol, interval="2h")[-1][last_futures_klines_param]) / float(
        #         client.futures_klines(symbol=symbol, interval="2h")[-2][penult_futures_klines_param]), 3) < 1:
        #     klines_2h.append(symbol)

        if round(float(client.futures_klines(symbol=symbol, interval="1h")[-1][last_futures_klines_param]) / float(
                client.futures_klines(symbol=symbol, interval="1h")[-2][penult_futures_klines_param]), 3) < 1:
            klines_1h.append(symbol)

        # if round(float(client.futures_klines(symbol=symbol, interval="30m")[-1][last_futures_klines_param]) / float(
        #         client.futures_klines(symbol=symbol, interval="30m")[-2][penult_futures_klines_param]), 3) < 1:
        #     klines_30m.append(symbol)

        # if round(float(client.futures_klines(symbol=symbol, interval="15m")[-1][last_futures_klines_param]) / float(
        #         client.futures_klines(symbol=symbol, interval="15m")[-2][penult_futures_klines_param]), 3) < 1:
        #     klines_15m.append(symbol)

        # if round(float(client.futures_klines(symbol=symbol, interval="5m")[-1][last_futures_klines_param]) / float(
        #         client.futures_klines(symbol=symbol, interval="5m")[-2][penult_futures_klines_param]), 3) < 1:
        #     klines_5m.append(symbol)

    result = set(klines_1h) & set(klines_6h) & set(klines_12h) & set(klines_1d)

    return list(result)


def set_greed():
    # set base_greed #
    base_greed = math.ceil(((float(client.futures_account()['totalWalletBalance']) * min_notional_corrector) / (
            len(get_futures_tickers_to_short()) * min_notional)))

    # get greed of last trade relative base_greed #
    income_and_time = {"income": [], "time": []}

    for x in client.futures_income_history():
        if x["incomeType"] == "REALIZED_PNL":
            income_and_time["income"].append(x["income"])
            income_and_time["time"].append(x["time"])

    income = income_and_time["income"][
        income_and_time["time"].index(
            max(income_and_time["time"]))]

    greed_of_last_trade = float(income) / (1 - base_percentage_futures_close) / (base_greed)

    # to increase or not based by last maker trade with realized_pnl #
    for x in client.futures_income_history():
        if x["incomeType"] == "REALIZED_PNL" and x["time"] > (serverTime - newest_edge):
            greed_of_last_trade = greed_of_last_trade + (base_greed * percentage_increase_of_base_greed)
            increased_base_greed = greed_of_last_trade
            break

        else:
            increased_base_greed = base_greed

    return min(round(increased_base_greed, 2), round((base_greed * times_base_greed_can_be_increased), 2))


def get_quantity(symbol):
    return round(
        (float(get_notional(symbol)) * set_greed())
        / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
        get_quantity_precision(symbol)
    )


def get_trade_fee(symbol):
    try:
        trade_fee = float(client.get_trade_fee(symbol=symbol)[0]["makerCommission"]) + float(
            client.get_trade_fee(symbol=symbol)[0]["takerCommission"])
    except Exception:
        trade_fee = float(client.get_trade_fee(symbol="BTCUSDT")[0]["makerCommission"]) + float(
            client.get_trade_fee(symbol="BTCUSDT")[0]["takerCommission"])

    return trade_fee


def create_open_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[2]["markPrice"])
                                                          * percentage_futures_open, get_tick_size(symbol)),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )
    except Exception:
        print("fail to open limit for", symbol)


def create_close_limit(symbol):
    try:
        client.futures_create_order(symbol=symbol,
                                    quantity=round_step_size(abs((float(
                                        client.futures_position_information(symbol=symbol)[2]["positionAmt"]))),
                                        get_step_size(symbol)),
                                    price=round_step_size(float(
                                        client.futures_position_information(symbol=symbol)[2]["entryPrice"])
                                                          * (base_percentage_futures_close - get_trade_fee(symbol)),
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


def get_last_isBuyerMaker_time():
    last_isBuyerMaker_time_sorting = {"time": []}
    for x in client.futures_ticker():
        for y in client.futures_account_trades(symbol=x["symbol"]):
            if y["side"] == "BUY":
                last_isBuyerMaker_time_sorting["time"].append(y["time"])

    return max(last_isBuyerMaker_time_sorting["time"])


last_realized_pnl_trade = get_last_isBuyerMaker_time()


##### --function open_for_profit #####
def open_for_profit():
    if last_realized_pnl_trade + newest_edge > serverTime or last_realized_pnl_trade + oldest_edge < serverTime:

        ####
        symbol_and_priceChangePercent = {"symbol": [], "priceChangePercent": []}
        for symbol in get_futures_tickers_to_short():
            symbol_and_priceChangePercent["symbol"].append(symbol)
            symbol_and_priceChangePercent["priceChangePercent"].append(
                round(float(client.futures_klines(symbol=symbol, interval=klines_interval)[-2][3]) / float(
                    client.futures_klines(symbol=symbol, interval=klines_interval)[-1][3]), 3)
            )

        symbol = symbol_and_priceChangePercent["symbol"][
            symbol_and_priceChangePercent["priceChangePercent"].index(
                min(symbol_and_priceChangePercent["priceChangePercent"]))]

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
