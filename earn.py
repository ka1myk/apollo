# TODO buy fixed products
import json
import time
from telegram_exception_alerts import Alerter
from binance.client import Client

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])


@tg_alert
def go_baby_earn():
    for x in variables['coin']:
        if float(client.get_asset_balance(asset=x)["free"]) > 0:
            try:
                client.purchase_lending_product(productId=x + str("001"),
                                                amount=float(client.get_asset_balance(asset=x)["free"]))
                time.sleep(1)
            except:
                print("Let's do it again")


go_baby_earn()
