import json
import secrets

from binance.client import Client
from binance.helpers import round_step_size

from telegram_exception_alerts import Alerter

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
tg_alert = Alerter(bot_token=variables['telegram']['bot_token'], chat_id=variables['telegram']['bot_chatID'])

for x in client.get_lending_product_list():
    if x["asset"] in variables['coin']:
        print(x["productId"])

for x in client.get_fixed_activity_project_list(type="CUSTOMIZED_FIXED"):
    if x["asset"] in variables['coin']:
        print(x["projectId"])
