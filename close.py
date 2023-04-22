import argparse
from binance.client import Client
from binance.helpers import round_step_size

parser = argparse.ArgumentParser()
parser.add_argument('--key', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
client = Client(parser.parse_args().key, parser.parse_args().secret)

budget_to_increase_greed = 2500
futures_limit_short_grid_close = [0.99]
futures_limit_short_grid_open = [1.03, 1.06, 1.09, 1.15, 1.21, 1.27, 1.39, 1.51, 1.63]

symbol_info = client.futures_exchange_info()


def close_grid_limit(symbol):
    def get_notional():
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'MIN_NOTIONAL':
                        return y['notional']

    def get_tick_size():
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'PRICE_FILTER':
                        return y['tickSize']

    def get_lot_size():
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'LOT_SIZE':
                        return y['stepSize']

    def get_quantity():
        quantity = round_step_size((float(get_notional()) / float(
            client.futures_mark_price(symbol=symbol)[
                "markPrice"])), get_lot_size())

        if float(quantity) < float(get_lot_size()):
            quantity = get_lot_size()

        return quantity

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
                                            "entryPrice"]) * (futures_limit_short_grid_close[x]),
                                                          get_tick_size()),
                                    side='BUY',
                                    positionSide='SHORT',
                                    type='LIMIT',
                                    timeInForce="GTC"
                                    )


def close_exist_positions():
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


def cancel_close_order_if_filled():
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

            if count_sell_orders != len(futures_limit_short_grid_open):
                for x in client.futures_get_open_orders(symbol=symbol):
                    if x["side"] == "BUY":
                        client.futures_cancel_order(symbol=symbol, orderId=x["orderId"])


def cancel_open_orders_without_position():
    open_orders = []
    positions = []

    for x in client.futures_get_open_orders():
        open_orders.append(x["symbol"])
    for y in client.futures_position_information():
        if float(y["positionAmt"]) < 0:
            positions.append(y["symbol"])

    for x in list(set(open_orders) - set(positions)):
        client.futures_cancel_all_open_orders(symbol=x)


cancel_close_order_if_filled()


close_exist_positions()
cancel_open_orders_without_position()





def open_grid_limit(symbol):
    def set_greed_and_min_notional_corrector():
        if float(client.futures_account()['totalWalletBalance']) < budget_to_increase_greed:
            greed = 1.2
        else:
            greed = round(float(client.futures_account()['totalWalletBalance']) / budget_to_increase_greed, 1)

        return greed

    def get_notional():
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'MIN_NOTIONAL':
                        return y['notional']

    def get_tick_size():
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'PRICE_FILTER':
                        return y['tickSize']

    def get_lot_size():
        for x in symbol_info['symbols']:
            if x['symbol'] == symbol:
                for y in x['filters']:
                    if y['filterType'] == 'LOT_SIZE':
                        return y['stepSize']

    def get_quantity():
        quantity = round_step_size((float(get_notional()) / float(
            client.futures_mark_price(symbol=symbol)[
                "markPrice"])) * set_greed_and_min_notional_corrector(), get_lot_size())

        if float(quantity) < float(get_lot_size()):
            quantity = get_lot_size()

        return quantity

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
