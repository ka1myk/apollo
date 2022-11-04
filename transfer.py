import json
from telegram_exception_alerts import Alerter
import numpy as np

from binance.client import BaseClient
from binance.client import Client

BaseClient.OPTIONS_URL = 'https://eapi.binance.{}/eapi'

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])

currency = variables['currency']
serverTime = client.get_server_time()['serverTime']
margin_all_pairs = client.get_margin_all_pairs()

pretty_qty = lambda x: np.format_float_positional(x, trim='-')


def get_free_currency_on_futures():
    for x in client.futures_account_balance():
        if x['asset'] == currency:
            return float(x['balance'])


# 1000 * 60 * 60 * 24 is interval for 24 hours
def profit_from_futures_to_spot():
    profit = client.futures_income_history(incomeType="REALIZED_PNL",
                                           startTime=serverTime - 1000 * 60 * 60 * 24,
                                           endTime=serverTime)

    for x in profit:
        client.futures_account_transfer(asset=variables['currency'],
                                        amount=float(x['income']),
                                        type=2,
                                        timestamp=serverTime)


def coin_from_spot_to_futures():
    coins = variables['coin'].keys()
    for x in coins:
        if float(client.get_asset_balance(asset=x)["free"]) > 0:
            client.futures_account_transfer(asset=x,
                                            amount=float(client.get_asset_balance(asset=x)["free"]),
                                            type=1,
                                            timestamp=serverTime)


def coin_from_margin_to_spot():
    for y in margin_all_pairs:
        for x in client.get_margin_trades(symbol=y["symbol"]):
            if x['isMaker'] == True and x["time"] > serverTime - 1000 * 60 * 60 * 24:
                client.transfer_margin_to_spot(asset=y["base"],
                                               amount=pretty_qty(float(x["qty"]) * 0.005))


def currency_from_option_to_spot():
    for x in client.options_user_trades():
        if round(float(x["realizedProfit"]), 1) > 0 and serverTime > float(x["time"]) > float(
                serverTime - (1000 * 60 * 60 * 24)):
            client.options_funds_transfer(currency="USDT", type="OUT", amount=round(float(x["realizedProfit"]), 1) / 2)


def usdt_to_busd_on_spot():
    if float(client.get_asset_balance(asset='USDT')['free']) > 10:
        client.create_order(symbol="BUSDUSDT",
                            side='BUY',
                            type='MARKET',
                            quoteOrderQty=round(float(client.get_asset_balance(asset='USDT')['free'])))


@tg_alert
def go_baby_transfer():
    coin_from_margin_to_spot()
    coin_from_spot_to_futures()
    currency_from_option_to_spot()
    usdt_to_busd_on_spot()
    if get_free_currency_on_futures() > 0:
        profit_from_futures_to_spot()


go_baby_transfer()
