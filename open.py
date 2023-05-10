from helper import *

symbol = secrets.choice(get_futures_tickers_to_short())
if get_usd_for_all_grid(symbol) <= availableBalance and get_usd_for_one_short(symbol) <= min_notional:
    set_futures_change_leverage(symbol)
    time.sleep(secrets.randbelow(secs_to_wait))
    client.futures_create_order(symbol=symbol,
                                quantity=get_quantity(symbol),
                                side='SELL',
                                positionSide='SHORT',
                                type='MARKET')