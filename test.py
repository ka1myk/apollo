import argparse
from binance.client import Client
from binance.helpers import round_step_size

parser = argparse.ArgumentParser()
parser.add_argument('--key', type=str, required=True)
parser.add_argument('--secret', type=str, required=True)
client = Client(parser.parse_args().key, parser.parse_args().secret)

budget_to_increase_greed = 1200


def set_greed_and_min_notional_corrector():
    if float(client.futures_account()['totalWalletBalance']) < budget_to_increase_greed:
        greed = 1.2
    else:
        greed = round(float(client.futures_account()['totalWalletBalance']) / budget_to_increase_greed, 1)

    return greed


def open_new_positions():

    symbol_and_priceChangePercent = {"symbol": [], "priceChangePercent": []}
    for x in client.futures_ticker():
        symbol_and_priceChangePercent["symbol"].append(x["symbol"])
        symbol_and_priceChangePercent["priceChangePercent"].append(float(x["priceChangePercent"]))

    exist_position = []
    for z in client.futures_position_information():
        if float(z["positionAmt"]) < 0:
            exist_position.append(z["symbol"])

    if symbol_and_priceChangePercent not in exist_position:

        x = range(-1, -int(set_greed_and_min_notional_corrector()), -1)
        for n in x:
            symbol_info = client.futures_exchange_info()
            client.futures_change_leverage(symbol=symbol_and_priceChangePercent["symbol"][
                symbol_and_priceChangePercent["priceChangePercent"].index(
                    sorted(symbol_and_priceChangePercent["priceChangePercent"])[
                        n])], leverage=1)

            def get_notional():
                for x in symbol_info['symbols']:
                    if x['symbol'] == symbol_and_priceChangePercent["symbol"][
                        symbol_and_priceChangePercent["priceChangePercent"].index(
                            sorted(symbol_and_priceChangePercent["priceChangePercent"])[
                                n])]:
                        for y in x['filters']:
                            if y['filterType'] == 'MIN_NOTIONAL':
                                return y['notional']

            def get_lot_size():
                for x in symbol_info['symbols']:
                    if x['symbol'] == symbol_and_priceChangePercent["symbol"][
                        symbol_and_priceChangePercent["priceChangePercent"].index(
                            sorted(symbol_and_priceChangePercent["priceChangePercent"])[
                                n])]:
                        for y in x['filters']:
                            if y['filterType'] == 'LOT_SIZE':
                                return y['stepSize']

            def get_quantity():
                quantity = round_step_size((float(get_notional()) / float(
                    client.futures_mark_price(symbol=symbol_and_priceChangePercent["symbol"][
                        symbol_and_priceChangePercent["priceChangePercent"].index(
                            sorted(symbol_and_priceChangePercent["priceChangePercent"])[
                                n])])[
                        "markPrice"])) * set_greed_and_min_notional_corrector(), get_lot_size())

                if float(quantity) < float(get_lot_size()):
                    quantity = get_lot_size()

                return quantity

            client.futures_create_order(symbol=symbol_and_priceChangePercent["symbol"][
                symbol_and_priceChangePercent["priceChangePercent"].index(
                    sorted(symbol_and_priceChangePercent["priceChangePercent"])[
                        n])],
                                        quantity=get_quantity(),
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='MARKET')


open_new_positions()
