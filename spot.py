#TODO add grid [-5%, -10%, -15%, -20%, -25%] of avg_price and refresh after each market buy
import argparse
import json

from binance.client import Client
from telegram_exception_alerts import Alerter

with open('variables.json') as v:
    variables = json.load(v)

parser = argparse.ArgumentParser()
parser.add_argument('--coin', type=str, required=True)
coin = parser.parse_args()

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
symbol = coin.coin + variables['currency']

bot_token = variables['telegram']['bot_token']
bot_chatID = variables['telegram']['bot_chatID']
tg_alert = Alerter(bot_token=bot_token, chat_id=bot_chatID)


def get_symbol_info():
    return client.get_symbol_info(symbol)


# why 13440?
# 7 * 40 * 4 * 12 = 13440$ for 12 month with greed 1, greed increase only by int
# len(coins) * week budget in $ * weeks in month * amount of month continuous trade
def set_greed():
    if float(client.get_asset_balance(asset='BUSD')['free']) < 13440:
        greed = 1
    else:
        greed = round(float(client.get_asset_balance(asset='BUSD')['free']) / 13440)
    return int(greed)


def get_min_notional():
    for y in get_symbol_info()['filters']:
        if y['filterType'] == 'MIN_NOTIONAL':
            return float(y['minNotional'])


@tg_alert
def go_baby_spot():
    client.order_market_buy(symbol=symbol, side='BUY', type='MARKET',
                            quoteOrderQty=get_min_notional() * set_greed())


go_baby_spot()
