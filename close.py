from helper import *


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
        print("fail to open_grid_limit", symbol)


def close_grid_limit(symbol):
    try:
        amount_of_close_orders = int(
            abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]) /
                float(get_quantity(symbol))))

        if amount_of_close_orders > len(futures_limit_short_grid_close):
            amount_of_close_orders = len(futures_limit_short_grid_close)

        for x in range(amount_of_close_orders):
            client.futures_create_order(symbol=symbol,
                                        quantity=round_step_size(abs((float(
                                            client.futures_position_information(symbol=symbol)[2][
                                                "positionAmt"]))) / int(
                                            amount_of_close_orders), get_lot_size(symbol)),
                                        activationPrice=round_step_size(float(
                                            client.futures_position_information(symbol=symbol)[2][
                                                "entryPrice"]) * (futures_limit_short_grid_close[x]),
                                                                        get_tick_size(symbol)),
                                        side='BUY',
                                        timeInForce="GTC",
                                        positionSide='SHORT',
                                        type='TRAILING_STOP_MARKET',
                                        callbackRate=callbackRate
                                        )
    except:
        print("fail to close_grid_limit", symbol)


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
        print("fail to close_exist_positions", symbol)


def cancel_close_order_if_filled():
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

                if count_sell_orders != len(futures_limit_short_grid_open):
                    for x in client.futures_get_open_orders(symbol=symbol):
                        if x["side"] == "BUY":
                            client.futures_cancel_order(symbol=symbol, orderId=x["orderId"])
    except:
        print("fail to cancel_close_order_if_filled", symbol)


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
        print("fail to cancel_open_orders_without_position")


cancel_close_order_if_filled()
close_exist_positions()
cancel_open_orders_without_position()
