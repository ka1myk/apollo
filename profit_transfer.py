import json
from decimal import *
from binance.client import Client

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

with open('variables.json') as v:
    variables = json.load(v)

profit_to_spot_multiplayer = variables['profit_to_spot_multiplayer']
hours_to_transfer_profit = variables['hours_to_transfer_profit']

profit = client.futures_income_history(incomeType="REALIZED_PNL",
                                       startTime=client.get_server_time()[
                                                     "serverTime"] - 1000 * 60 * 60 * hours_to_transfer_profit,
                                       endTime=client.get_server_time()["serverTime"])

for x in profit:
    client.futures_account_transfer(asset="BUSD",
                                    amount=Decimal(x["income"]) * Decimal(profit_to_spot_multiplayer),
                                    type=2,
                                    timestamp=client.get_server_time()["serverTime"])
