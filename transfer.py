# TODO endless process
# TODO remove numpy import
import json
from telegram_exception_alerts import Alerter
import numpy as np

from binance.client import Client

with open('/root/apollo/variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])

currency = variables['currency']
serverTime = client.get_server_time()['serverTime']
margin_all_pairs = client.get_margin_all_pairs()
coins = variables['coin']

pretty_qty = lambda x: np.format_float_positional(x, trim='-')


def get_free_currency_on_futures():
    for x in client.futures_account_balance():
        if x['asset'] == currency and float(x['balance']) > 0:
            return True


def get_free_coin_on_margin():
    for x in coins:
        for y in client.get_margin_account()["userAssets"]:
            if y["asset"] in x and y["free"] == 0:
                return True


# 1000 * 60 * 60 * 24 is interval for 24 hours
def currency_from_futures_to_spot():
    profit = client.futures_income_history(incomeType="REALIZED_PNL",
                                           startTime=serverTime - 1000 * 60 * 60 * 24,
                                           endTime=serverTime)

    for x in profit:
        client.futures_account_transfer(asset=variables['currency'],
                                        amount=float(x['income']),
                                        type=2,
                                        timestamp=serverTime)


def coin_from_spot_to_futures():
    for x in coins:
        if float(client.get_asset_balance(asset=x)["free"]) > 0:
            client.futures_account_transfer(asset=x,
                                            amount=float(client.get_asset_balance(asset=x)["free"]),
                                            type=1,
                                            timestamp=serverTime)


def coin_from_spot_to_margin():
    for x in coins:
        if float(client.get_asset_balance(asset=x)["free"]) > 0:
            client.transfer_spot_to_margin(asset=x,
                                           amount=float(client.get_asset_balance(asset=x)["free"]))


def coin_from_margin_to_spot():
    for y in margin_all_pairs:
        for x in client.get_margin_trades(symbol=y["symbol"]):
            if x['isMaker'] is True and x["time"] > serverTime - 1000 * 60 * 60 * 24:
                client.transfer_margin_to_spot(asset=y["base"],
                                               amount=pretty_qty(float(x["qty"]) * 0.005))


@tg_alert
def go_baby_transfer():
    if get_free_coin_on_margin():
        coin_from_spot_to_margin()
    coin_from_margin_to_spot()
    coin_from_spot_to_futures()
    if get_free_currency_on_futures():
        currency_from_futures_to_spot()


go_baby_transfer()
