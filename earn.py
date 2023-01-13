import json
import secrets
import time

from binance.client import Client

from telegram_exception_alerts import Alerter

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])
coins = variables['coin']
free_coins_on_spot = []

for x in coins:
    if float(client.get_asset_balance(asset=x)["free"]) > 0:
        free_coins_on_spot.append(x)

if secrets.randbelow(2) == 1:
    for x in client.get_lending_product_list():
        for y in free_coins_on_spot:
            if x["asset"] in free_coins_on_spot and float(client.get_asset_balance(asset=y)["free"]) > float(
                    x["minPurchaseAmount"]):
                print(x["productId"], float(x["minPurchaseAmount"]))
                client.purchase_lending_product(productId=x["productId"], amount=float(x["minPurchaseAmount"]))
                time.sleep(5)

else:
    for x in client.get_fixed_activity_project_list(type="CUSTOMIZED_FIXED"):
        for y in free_coins_on_spot:
            if float(client.get_asset_balance(asset=y)["free"]) > float(x["lotSize"]):
                print(x["projectId"], float(x["lotSize"]))
                client.purchase_lending_product(projectId=x["projectId"], lot=float(x["lotSize"]))
                time.sleep(5)
