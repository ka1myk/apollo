import json

from binance.client import Client

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])
currency = variables['currency']


def get_free_currency():
    for x in client.futures_account_balance():
        if x['asset'] == currency:
            return float(x['balance'])


# 1000 * 60 * 60 * 24 is interval for 24 hours

def busd_from_futures_to_spot():
    profit = client.futures_income_history(incomeType="REALIZED_PNL",
                                           startTime=client.get_server_time()[
                                                         'serverTime'] - 1000 * 60 * 60 * 24,
                                           endTime=client.get_server_time()['serverTime'])

    for x in profit:
        client.futures_account_transfer(asset="BUSD",
                                        amount=float(x['income']),
                                        type=2,
                                        timestamp=client.get_server_time()['serverTime'])


def coin_from_spot_to_futures():
    coins = variables['coin'].keys()
    for x in coins:
        if float(client.get_asset_balance(asset=x)["free"]) > 0:
            client.futures_account_transfer(asset=x,
                                            amount=float(client.get_asset_balance(asset=x)["free"]),
                                            type=1,
                                            timestamp=client.get_server_time()["serverTime"])


coin_from_spot_to_futures()
if get_free_currency() > 0:
    busd_from_futures_to_spot()
