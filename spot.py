# TODO add binance another user as argument
import json
import secrets
from binance.client import Client
from binance.helpers import round_step_size
from telegram_exception_alerts import Alerter

with open('/root/apollo/variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])


# if margin trading or not - choose symbol to buy#
if float(client.get_margin_account()["totalAssetOfBtc"]) != 0:
    my_dict = {"coin": [], "balance": []}
    for x in client.get_margin_account()["userAssets"]:
        if float(x["netAsset"]) != 0:
            my_dict["coin"].append(x["asset"])
            my_dict["balance"].append(round(
                float(x["netAsset"]) * float(
                    client.get_avg_price(symbol=x["asset"] + variables['currency'])['price']), 4))

    symbol = my_dict["coin"][my_dict["balance"].index(min(my_dict["balance"]))] + variables['currency']

else:

    symbol = secrets.choice(variables['coin']) + variables['currency']

symbol_info = client.get_symbol_info(symbol)


def set_greed():
    if float(client.get_asset_balance(asset=variables['currency'])['free']) < variables[
        'budget_up_to_1_greed']:
        greed = variables['greed']
    else:
        greed = round(float(client.get_asset_balance(asset=variables['currency'])['free']) / variables[
            'budget_up_to_1_greed'])
    return greed


def get_min_notional():
    for x in symbol_info["filters"]:
        if x['filterType'] == 'MIN_NOTIONAL':
            return x['minNotional']


def get_tick_size():
    for x in symbol_info["filters"]:
        if x['filterType'] == 'PRICE_FILTER':
            return x['tickSize']


def get_lot_size():
    for x in symbol_info["filters"]:
        if x['filterType'] == 'LOT_SIZE':
            return x['stepSize']


def spot_cancel_orders():
    for x in client.get_open_orders(symbol=symbol):
        client.cancel_order(symbol=symbol, orderId=x["orderId"])


def spot_create_market_buy():
    client.order_market_buy(symbol=symbol,
                            quoteOrderQty=float(get_min_notional()) * set_greed(),
                            side='BUY',
                            type='MARKET'
                            )


def spot_create_grid_limit_buy(grid):
    for x in grid:
        client.order_limit(symbol=symbol,
                           quantity=round_step_size(float(client.get_all_orders(symbol=symbol)[-1]["origQty"]) * 1 / x,
                                                    get_lot_size()),
                           price=round_step_size(float(client.get_avg_price(symbol=symbol)['price']) * x,
                                                 get_tick_size()),
                           side='BUY',
                           type='LIMIT',
                           timeInForce="GTC"
                           )


@tg_alert
def go_baby_spot():
    spot_cancel_orders()
    spot_create_market_buy()
    spot_create_grid_limit_buy(variables['spot_limit_long_grid'])


go_baby_spot()
