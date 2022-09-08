import json
from binance.client import Client

with open('variables.json') as v:
    variables = json.load(v)

eth_to_buy_multiplayer = variables['eth_to_buy_multiplayer']
btc_to_buy_multiplayer = variables['btc_to_buy_multiplayer']
bnb_to_buy_multiplayer = variables['bnb_to_buy_multiplayer']

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

eth_buy_order = client.order_market_buy(
    symbol='ETHBUSD',
    quantity=100)

btc_buy_order = client.order_market_buy(
    symbol='BTCBUSD',
    quantity=100)

bnb_buy_order = client.order_market_buy(
    symbol='BNBBUSD',
    quantity=100)