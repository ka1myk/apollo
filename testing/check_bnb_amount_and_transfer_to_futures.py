import json
from binance.client import Client

with open('variables.json') as v:
    variables = json.load(v)

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

bnb_amount_to_transfer_from_spot = variables['bnb_amount_to_transfer_from_spot']
bnb_balance_on_spot = client.get_asset_balance(asset='BNB')["free"]


def get_futures_wallet_balance(pair):
    for x in client.futures_account()['assets']:
        if x['asset'] == pair:
            return x['walletBalance']


bnb_balance_on_futures = get_futures_wallet_balance('BNB')
print('bnb_balance_on_futures', bnb_balance_on_futures, 'bnb_amount_to_transfer_from_spot',
      bnb_amount_to_transfer_from_spot,
      'bnb_balance_on_spot', bnb_balance_on_spot)

if float(bnb_balance_on_futures) < float(bnb_amount_to_transfer_from_spot) < float(bnb_balance_on_spot):
    client.futures_account_transfer(asset="BNB",
                                    amount=bnb_amount_to_transfer_from_spot,
                                    type=1,
                                    timestamp=client.get_server_time()["serverTime"])
