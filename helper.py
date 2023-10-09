import random, re, math, secrets, argparse

from binance.client import Client
from binance.helpers import round_step_size

client = Client("",
                "")

asset = "USDT"
# default = 6; min_notional can be extended #
min_notional = 10
# default = 1.2; min_notional_corrector needs to correct error of not creating close orders #
min_notional_corrector = 1.2

# for short without fee deduction #
short_base_percentage_futures_close = 0.999
# for long without fee deduction#
long_base_percentage_futures_close = 1.001

# all tickers ~ 200, 200 for long and 200 for short, so percentage_of_open_position is for x * 200 * 2  #
percentage_of_open_position = 1
# tickers in one deal #
quantity_at_a_time = 5

# last digit is for min #
last_timeframe_in_min = 1000 * 60 * 120

# last digit is for days #
deltaTime = 1000 * 60 * 60 * 24 * 14
# most likely, it will not fall less than 0.79, so lower limit orders will be cancelled after deltaTime #
percentage_spot_open = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]

futures_ticker = client.futures_ticker()
symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']
futures_account_balance = client.futures_account_balance()
futures_position_information = client.futures_position_information()

check_symbol = "BTCUSDT"
binance_spot = float(client.get_symbol_ticker(symbol=check_symbol)["price"])
binance_spot_5_min = float(client.get_avg_price(symbol=check_symbol)["price"])
binance_spot_24_h = float(client.get_ticker(symbol=check_symbol)["weightedAvgPrice"])
binance_futures = float(client.futures_mark_price(symbol=check_symbol)["markPrice"])


def set_futures_change_leverage():
    for x in futures_ticker:
        try:
            print(client.futures_change_leverage(symbol=x["symbol"], leverage=1))
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
        if float(x["onboardDate"]) > serverTime - deltaTime:
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
        # set base_greed #
        # base_greed = math.ceil(((float(futures_account['totalWalletBalance']) * min_notional_corrector) / (
        #         len(futures_ticker) * min_notional)))

        base_greed = min_notional_corrector

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
            if x["time"] < serverTime - deltaTime:
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


# --function transfer_profit #

def transfer_profit():
    transfer_free_USD_to_spot()
    buy_coins_on_spot()
    transfer_free_spot_coin_to_futures()


def count_open_positions_and_start():
    long_trades_in_last_timeframe = 0
    short_trades_in_last_timeframe = 0

    for x in client.futures_account_trades():
        if float(x["time"]) > serverTime - last_timeframe_in_min and float(x["realizedPnl"]) > 0 and x["side"] == "SELL":
            long_trades_in_last_timeframe = long_trades_in_last_timeframe + 1
        if float(x["time"]) > serverTime - last_timeframe_in_min and float(x["realizedPnl"]) > 0 and x["side"] == "BUY":
            short_trades_in_last_timeframe = short_trades_in_last_timeframe + 1

    if long_trades_in_last_timeframe > short_trades_in_last_timeframe:
        for i in range(quantity_at_a_time):
            try:
                symbol = random.choice(short_get_futures_tickers)
                short(symbol)
                short_get_futures_tickers.remove(symbol)
            except Exception as e:
                print(e)

    if short_trades_in_last_timeframe > long_trades_in_last_timeframe:
        for i in range(quantity_at_a_time):
            try:
                symbol = random.choice(long_get_futures_tickers)
                long(symbol)
                long_get_futures_tickers.remove(symbol)
            except Exception as e:
                print(e)

    # if long_trades_in_last_timeframe == short_trades_in_last_timeframe:
    #
    #     long_positions = 0
    #     for x in futures_position_information:
    #         if float(x["positionAmt"]) > 0:
    #             long_positions = long_positions + 1
    #
    #     short_positions = 0
    #     for x in futures_position_information:
    #         if float(x["positionAmt"]) < 0:
    #             short_positions = short_positions + 1
    #
    #     if (round((long_positions + short_positions) / (len(get_futures_tickers) * 2), 2)) < percentage_of_open_position:
    #         if binance_spot < binance_spot_5_min:
    #             for i in range(quantity_at_a_time):
    #                 try:
    #                     symbol = random.choice(short_get_futures_tickers)
    #                     short(symbol)
    #                     short_get_futures_tickers.remove(symbol)
    #                 except Exception as e:
    #                     print(e)
    #
    #         else:
    #             for i in range(quantity_at_a_time):
    #                 try:
    #                     symbol = random.choice(long_get_futures_tickers)
    #                     long(symbol)
    #                     long_get_futures_tickers.remove(symbol)
    #                 except Exception as e:
    #                     print(e)


def long(trade_symbol):
    client.futures_create_order(symbol=trade_symbol,
                                quantity=get_quantity(trade_symbol),
                                side='BUY',
                                positionSide='LONG',
                                type='MARKET'
                                )

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


def short(trade_symbol):
    client.futures_create_order(symbol=trade_symbol,
                                quantity=get_quantity(trade_symbol),
                                side='SELL',
                                positionSide='SHORT',
                                type='MARKET'
                                )

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


parser = argparse.ArgumentParser()
parser.add_argument('--function', type=str, required=True)

if parser.parse_args().function == "open":
    count_open_positions_and_start()
if parser.parse_args().function == "transfer":
    transfer_profit()
if parser.parse_args().function == "initialized":
    set_futures_change_multi_assets_mode()
    set_futures_change_leverage()
