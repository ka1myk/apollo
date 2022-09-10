import json
from binance.client import Client
from secrets import randbelow

with open('variables.json') as v:
    variables = json.load(v)

btc_to_buy_multiplayer = variables['btc_to_buy_multiplayer']

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

avg_price = client.get_avg_price(symbol='BNBBUSD')

### bnb market buy on BUSD ###

bnb_market_buy = client.order_market_buy(
    symbol='BNBBUSD',
    quantity=0.037)

### availible bnb limit sell ###

bnb_limit_sell = client.order_limit_sell(
    symbol='BNBBUSD',
    quantity=0.037,
    price=round(float(avg_price['price']) * round(randbelow(30) * 0.01 + 1.02, 3), 1))
