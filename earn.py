import json
import secrets

from binance.client import Client

from telegram_exception_alerts import Alerter

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])
coins = variables['coin']
free_coins_on_spot = []
coins_flexible = []
coins_fixed = []

for x in coins:
    if float(client.get_asset_balance(asset=x)["free"]) > 0:
        free_coins_on_spot.append(x)

for x in client.get_lending_product_list():
    for y in free_coins_on_spot:
        if x["asset"] in free_coins_on_spot and float(client.get_asset_balance(asset=y)["free"]) > float(
                x["minPurchaseAmount"]):
            coins_flexible.append(x["productId"])

for x in client.get_fixed_activity_project_list(type="CUSTOMIZED_FIXED"):
    if x["asset"] in free_coins_on_spot and float(client.get_asset_balance(asset=y)["free"]) > float(x["lotSize"]):
        coins_fixed.append(x["projectId"])

#if secrets.randbelow(2) == 1:
    # print(secrets.choice(list(dict.fromkeys(coins_flexible))))
client.purchase_lending_product(productId=secrets.choice(list(dict.fromkeys(coins_flexible))), amount="")
#else:
#    print(secrets.choice(list(dict.fromkeys(coins_fixed))))
