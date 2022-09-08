import json
from decimal import *
from binance.client import Client

with open('variables.json') as v:
    variables = json.load(v)

profit_to_spot_multiplayer = variables['profit_to_spot_multiplayer']

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

timeframe_in_hours = 6

profit = (client.futures_income_history(incomeType="REALIZED_PNL",
                                        startTime=client.get_server_time()[
                                                      "serverTime"] - 1000 * 60 * 60 * timeframe_in_hours,
                                        endTime=client.get_server_time()["serverTime"]))

def get_and_transfer_REALIZED_PNL():
    for x in profit:
        print(x["symbol"], x["income"])
        # print(client.futures_account_transfer(asset="BUSD",
        #                                 amount=Decimal(x["income"]) * Decimal(profit_to_spot_multiplayer),
        #                                 type=2,
        #                                 timestamp=client.get_server_time()["serverTime"]))

get_and_transfer_REALIZED_PNL()
