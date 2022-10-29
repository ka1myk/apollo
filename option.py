import json

from binance.client import BaseClient
from binance.client import Client

BaseClient.OPTIONS_URL = 'https://eapi.binance.{}/eapi'

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])

serverTime = float(client.options_time()["serverTime"])
avg_price = float(client.get_avg_price(symbol="ETHUSDT")['price'])

for x in client.options_exchange_info()["optionSymbols"]:
    if float(x["expiryDate"]) > serverTime + (1000 * 60 * 60 * 24 * 70) and \
            x["side"] == "CALL" and \
            float(x["strikePrice"]) > avg_price * 1.3:
        markPrice = float(client.options_mark_price(symbol=x["symbol"])[0]["markPrice"])
        client.options_place_order(symbol=x["symbol"], side="BUY", type="LIMIT", quantity=x["minQty"], price=markPrice)
