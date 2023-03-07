import re
import time
import argparse
from binance.client import Client
from binance.helpers import round_step_size

parser = argparse.ArgumentParser()
parser.add_argument('--key', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
client = Client(parser.parse_args().key, parser.parse_args().secret)

priceChangePercent = 10
budget_to_increase_greed = 1200
futures_limit_short_grid_close = [0.99, 0.97, 0.94, 0.90, 0.85, 0.79, 0.72, 0.64, 0.55]
serverTime = client.get_server_time()['serverTime']


def set_greed_and_min_notional_corrector():
    if float(client.futures_account()['totalWalletBalance']) < budget_to_increase_greed:
        greed = 1.2
    else:
        greed = round(float(client.futures_account()['totalWalletBalance']) / budget_to_increase_greed, 1)
    return greed


def futures_short():
    for z in client.futures_ticker():
        if float(z["priceChangePercent"]) > float(priceChangePercent):
            try:
                symbol_info = client.futures_exchange_info()
                client.futures_change_leverage(symbol=z["symbol"], leverage=1)

                def get_fees():
                    return float(client.get_trade_fee(symbol=z["symbol"])[0]["makerCommission"]) + float(
                        client.get_trade_fee(symbol=z["symbol"])[0]["takerCommission"])

                def get_notional():
                    for x in symbol_info['symbols']:
                        if x['symbol'] == z["symbol"]:
                            for y in x['filters']:
                                if y['filterType'] == 'MIN_NOTIONAL':
                                    return y['notional']

                def get_tick_size():
                    for x in symbol_info['symbols']:
                        if x['symbol'] == z["symbol"]:
                            for y in x['filters']:
                                if y['filterType'] == 'PRICE_FILTER':
                                    return y['tickSize']

                def get_lot_size():
                    for x in symbol_info['symbols']:
                        if x['symbol'] == z["symbol"]:
                            for y in x['filters']:
                                if y['filterType'] == 'LOT_SIZE':
                                    return y['stepSize']

                def get_quantity():
                    quantity = round_step_size((float(get_notional()) / float(
                        client.futures_mark_price(symbol=z["symbol"])[
                            "markPrice"])) * set_greed_and_min_notional_corrector(), get_lot_size())

                    if float(quantity) < float(get_lot_size()):
                        quantity = get_lot_size()

                    return quantity

                client.futures_create_order(symbol=z["symbol"],
                                            quantity=get_quantity(),
                                            side='SELL',
                                            positionSide='SHORT',
                                            type='MARKET')

                client.futures_cancel_all_open_orders(symbol=z["symbol"])
                time.sleep(2)

                amount_of_close_orders = int(
                    abs(float(client.futures_position_information(symbol=z["symbol"])[2]["positionAmt"]) /
                        float(get_quantity())))

                if amount_of_close_orders > len(futures_limit_short_grid_close):
                    amount_of_close_orders = len(futures_limit_short_grid_close)

                for x in range(amount_of_close_orders):
                    client.futures_create_order(symbol=z["symbol"],
                                                quantity=round_step_size(abs((float(
                                                    client.futures_position_information(symbol=z["symbol"])[2][
                                                        "positionAmt"]))) / int(
                                                    amount_of_close_orders), get_lot_size()),
                                                price=round_step_size(float(
                                                    client.futures_position_information(symbol=z["symbol"])[2][
                                                        "entryPrice"]) * (futures_limit_short_grid_close[
                                                                              x] - get_fees()),
                                                                      get_tick_size()),
                                                side='BUY',
                                                positionSide='SHORT',
                                                type='LIMIT',
                                                timeInForce="GTC"
                                                )


            except:
                print("futures_short")


def is_short_position_on_futures():
    for x in client.futures_position_information():
        if float(x["positionAmt"]) != 0:
            return True


def currency_from_futures_to_spot():
    for x in client.futures_account_balance():
        matchObj = re.search("^((?!USD).)*$", x["asset"])
        if not matchObj:
            try:
                client.futures_account_transfer(asset=x["asset"],
                                                amount=float(x['withdrawAvailable']),
                                                type=2,
                                                timestamp=serverTime)
            except:
                print("currency_from_futures_to_spot.futures_account_transfer")


def get_undervalued_asset():
    my_dict = {"symbol": [], "balance": []}
    for x in client.futures_account_balance():
        matchObj = re.search("^((?!USD).)*$", x["asset"])
        if matchObj:
            symbol = x["asset"] + 'USDT'
            candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MONTH)
            avg_price = client.get_avg_price(symbol=symbol)["price"]

            my = 0
            ny = 0

            for y in candles:
                my = my + float(y[4])
                ny = ny + 1

            my_dict["symbol"].append(x["asset"])
            my_dict["balance"].append(round(float(avg_price) / (my / ny), 2))
    symbol = my_dict["symbol"][my_dict["balance"].index(min(my_dict["balance"]))]

    return symbol


def spot_long():
    for x in client.get_account()["balances"]:
        matchObj = re.search("^((?!USD).)*$", x["asset"])
        if not matchObj and float(x["free"]) > 10:

            try:
                client.order_market_buy(symbol=get_undervalued_asset() + x["asset"],
                                        quoteOrderQty=float(x["free"]),
                                        side='BUY',
                                        type='MARKET'
                                        )
            except:
                print("spot_long.order_market_buy")


def coin_from_spot_to_futures():
    for x in client.futures_account_balance():
        if float(client.get_asset_balance(asset=x["asset"])["free"]) > 0:
            try:
                client.futures_account_transfer(asset=x["asset"],
                                                amount=float(client.get_asset_balance(asset=x["asset"])["free"]),
                                                type=1,
                                                timestamp=serverTime)
            except:
                print("coin_from_spot_to_futures.futures_account_transfer")


futures_short()
if not is_short_position_on_futures():
    currency_from_futures_to_spot()
spot_long()
coin_from_spot_to_futures()
