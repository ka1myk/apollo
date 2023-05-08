from helper import *

with open('variables.json') as v:
    shortReady = json.load(v)


def open_new_positions():
    if budgetContract < availableBalance:
        symbol = secrets.choice(shortReady)
        futures_change_leverage(symbol)
        time.sleep(secrets.randbelow(max_secs_to_wait_before_new_position))
        client.futures_create_order(symbol=symbol,
                                    quantity=get_quantity(symbol),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='MARKET')


open_new_positions()
