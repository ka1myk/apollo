import re, time, math, secrets, argparse
from binance.client import Client
from binance.helpers import round_step_size

parser = argparse.ArgumentParser()
parser.add_argument('--function', type=str, required=True)

client = Client("",
                "")

# min_notional can be extended #
min_notional = 10
# min_notional_corrector need to correct error of not creating close orders #
min_notional_corrector = 1.2
# 60 secs * minutes #
secs_to_wait = 60 * 59
futures_close_profit = [0.995]
futures_open_short = [1.10]
# last digit is for days to cancel not filled limit orders #
deltaTime = 1000 * 60 * 60 * 24 * 7
# most likely, it will not fall less than 0.79, so lower limit orders can be cancelled and moved to funding #
spot_open_long = [0.97, 0.94, 0.91, 0.85, 0.79, 0.73]

symbol_info = client.futures_exchange_info()
serverTime = client.get_server_time()['serverTime']
availableBalance = round(float(client.futures_account()["availableBalance"]))


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


def get_futures_tickers_to_short():
    futures_account_balance_asset = []
    for x in client.futures_account_balance():
        futures_account_balance_asset.append(x["asset"] + "USDT")

    all_tickers = []
    for futures in client.futures_ticker():
        remove_quarterly_contract = re.search('^((?!_).)*$', futures["symbol"])
        remove_busd_contract = re.search('^.*USDT$', futures["symbol"])
        if remove_quarterly_contract and remove_busd_contract:
            all_tickers.append(futures["symbol"])

    exist_positions = []
    for z in client.futures_position_information():
        if float(z["positionAmt"]) < 0:
            exist_positions.append(z["symbol"])

    short_ready = set(all_tickers) - set(exist_positions) - set(futures_account_balance_asset)

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
        for y in client.futures_position_information():
            if float(y["positionAmt"]) < 0:
                positions.append(y["symbol"])

        for x in list(set(open_orders) - set(positions)):
            client.futures_cancel_all_open_orders(symbol=x)

    except Exception:
        print("fail to cancel open orders without position for", open_orders)


def transfer_free_USD_to_spot():
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


def usdt_to_busd_on_spot():
    if float(client.get_asset_balance(asset='USDT')['free']) > 10:
        try:
            client.create_order(symbol="BUSDUSDT",
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=math.floor(float(client.get_asset_balance(asset='USDT')['free'])))

            dust_to_bnb()
        except Exception:
            print("fail to convert USDT to BUSD")


def dust_to_bnb():
    try:
        client.transfer_dust(asset="USDT")
    except Exception:
        print("fail to dust USDT to BNB")


def buy_coins_on_spot():
    symbol = "BTCBUSD"

    for x in client.get_open_orders(symbol=symbol):
        if x["time"] < serverTime - deltaTime:
            client.cancel_order(symbol=symbol, orderId=x["orderId"])

    if 10 < float(client.get_asset_balance(asset='BUSD')['free']) < 20:
        try:
            client.create_order(symbol=symbol,
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=float(client.get_asset_balance(asset='BUSD')['free']))
        except Exception:
            print("fail to buy market BTC for BUSD")

    if float(client.get_asset_balance(asset='BUSD')['free']) > 20:
        try:
            client.create_order(symbol=symbol,
                                side='BUY',
                                type='MARKET',
                                quoteOrderQty=math.floor(float(client.get_asset_balance(asset='BUSD')['free']) * 0.5))

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
            print("fail to buy limit BTC for BUSD")


def transfer_free_spot_coin_to_futures():
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


##### --function open_for_profit #####
def open_for_profit():
    time.sleep(secrets.randbelow(secs_to_wait))
    for symbol in get_futures_tickers_to_short():
        try:
            if get_usd_for_all_grid(symbol) <= availableBalance and get_usd_for_one_short(symbol) <= min_notional:
                set_futures_change_leverage(symbol)
                client.futures_create_order(symbol=symbol,
                                            quantity=get_quantity(symbol),
                                            side='SELL',
                                            positionSide='SHORT',
                                            type='MARKET')
        except Exception:
            print("fail open short", symbol)

##### --function close_with_profit #####
def close_with_profit():
    cancel_close_order_if_filled()
    close_exist_positions()
    cancel_open_orders_without_position()


##### --function transfer_profit #####
def transfer_profit():
    transfer_free_USD_to_spot()
    usdt_to_busd_on_spot()
    buy_coins_on_spot()
    transfer_free_spot_coin_to_futures()


if parser.parse_args().function == "open":
    open_for_profit()
if parser.parse_args().function == "close":
    close_with_profit()
if parser.parse_args().function == "transfer":
    transfer_profit()
