from helper import *


def open_new_positions():
    if budgetContract < availableBalance:
        symbol = secrets.choice(shortReady)
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='MARKET')


open_new_positions()
