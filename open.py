from helper import *

symbol = secrets.choice(futures_tickers_to_short())


def open_new_position():
    if get_budget_contract(symbol) <= availableBalance and budget_to_one_short(symbol) <= min_notional:
        futures_change_leverage(symbol)
        time.sleep(secrets.randbelow(max_secs_to_wait_before_new_position))
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='MARKET')

        create_trailing_stop()


def create_trailing_stop():
    client.futures_create_order(symbol=symbol,
                                quantity=round_step_size(abs((float(
                                    client.futures_position_information(symbol=symbol)[2][
                                        "positionAmt"]))), get_step_size(symbol)),
                                activationPrice=round_step_size(float(
                                    client.futures_position_information(symbol=symbol)[2][
                                        "entryPrice"]) * futures_limit_short_grid_close,
                                                                get_tick_size(symbol)),
                                side='BUY',
                                timeInForce="GTC",
                                positionSide='SHORT',
                                type='TRAILING_STOP_MARKET',
                                callbackRate=callbackRate
                                )


open_new_position()
