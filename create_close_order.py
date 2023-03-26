import re
import time
import argparse
from binance.client import Client
from binance.helpers import round_step_size

parser = argparse.ArgumentParser()
parser.add_argument('--key', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
client = Client(parser.parse_args().key, parser.parse_args().secret)

budget_to_increase_greed = 1200
futures_limit_short_grid_close = [0.99]
futures_limit_short_grid_open = [1.05, 1.10, 1.20, 1.35]
serverTime = client.get_server_time()['serverTime']

for z in client.futures_position_information():
    if float(z["positionAmt"]) < 0:
        count_buy_orders = 0
        count_sell_orders = 0
        symbol = z["symbol"]

        for x in client.futures_get_open_orders(symbol=symbol):
            if x["side"] == "BUY":
                count_buy_orders = count_buy_orders + 1
            if x["side"] == "SELL":
                count_sell_orders = count_sell_orders + 1

        if count_buy_orders != len(futures_limit_short_grid_close):
            client.futures_cancel_all_open_orders(symbol=symbol)
            break

        if count_sell_orders != len(futures_limit_short_grid_open):
            symbol_info = client.futures_exchange_info()
            client.futures_change_leverage(symbol=symbol, leverage=1)


            def set_greed_and_min_notional_corrector():
                # if float(client.futures_account()['totalWalletBalance']) < budget_to_increase_greed:
                #     greed = 1.2
                # else:
                #     greed = round(float(client.futures_account()['totalWalletBalance']) / budget_to_increase_greed,
                #                   1)

                greed = 1.2
                return greed


            def get_notional():
                for x in symbol_info['symbols']:
                    if x['symbol'] == symbol:
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


            client.futures_cancel_all_open_orders(symbol=symbol)

            for x in futures_limit_short_grid_open:
                client.futures_create_order(symbol=symbol,
                                            quantity=get_quantity(),
                                            price=round_step_size(float(
                                                client.futures_position_information(symbol=symbol)[2][
                                                    "markPrice"]) * (
                                                                      x),
                                                                  get_tick_size()),
                                            side='SELL',
                                            positionSide='SHORT',
                                            type='LIMIT',
                                            timeInForce="GTC"
                                            )

            amount_of_close_orders = int(
                abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]) /
                    float(get_quantity())))

            if amount_of_close_orders > len(futures_limit_short_grid_close):
                amount_of_close_orders = len(futures_limit_short_grid_close)

            for x in range(amount_of_close_orders):
                client.futures_create_order(symbol=symbol,
                                            quantity=round_step_size(abs((float(
                                                client.futures_position_information(symbol=symbol)[2][
                                                    "positionAmt"]))) / int(
                                                amount_of_close_orders), get_lot_size()),
                                            price=round_step_size(float(
                                                client.futures_position_information(symbol=symbol)[2][
                                                    "entryPrice"]) * (futures_limit_short_grid_close[
                                                x]),
                                                                  get_tick_size()),
                                            side='BUY',
                                            positionSide='SHORT',
                                            type='LIMIT',
                                            timeInForce="GTC"
                                            )
