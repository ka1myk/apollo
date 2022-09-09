import json
from binance.client import Client

with open('variables.json') as v:
    variables = json.load(v)

btc_to_buy_multiplayer = variables['btc_to_buy_multiplayer']

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

avg_price = client.get_avg_price(symbol='BNBBUSD')

### bnb market buy on BUSD ###

order = client.order_market_buy(
    symbol='BNBBUSD',
    quantity=0.037)

### availible bnb limit sell ###

btc_limit_sell_availible = client.order_limit_sell(
    symbol='BNBBUSD',
    quantity=0.037,
    price=round(float(avg_price['price']) * 1.05, 1))