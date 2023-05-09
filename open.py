from helper import *


def open_new_position():
    symbol = secrets.choice(futures_tickers_to_short())
    if get_budget_contract(symbol) <= availableBalance and budget_to_one_short(symbol) <= min_notional:
        futures_change_leverage(symbol)
        time.sleep(secrets.randbelow(max_secs_to_wait_before_new_position))
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='MARKET')


open_new_position()
