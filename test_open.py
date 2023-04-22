from helper import *


def open_new_positions():
    try:
        if budgetContract < availableBalance:
            symbol = secrets.choice(futures_tickers_to_short())
            client.futures_create_order(symbol=symbol,
                                        quantity=get_quantity(symbol),
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='MARKET')

    except:
        print("open_new_positions fail with", symbol)


open_new_positions()
