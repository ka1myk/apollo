import json
from binance.client import Client
from secrets import randbelow

with open('variables.json') as v:
    variables = json.load(v)

btc_to_buy_multiplayer = variables['btc_to_buy_multiplayer']

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

avg_price_bnb = client.get_avg_price(symbol='BNBBUSD')
avg_price_eth = client.get_avg_price(symbol='ETHBUSD')
avg_price_btc = client.get_avg_price(symbol='BTCBUSD')

### bnb market buy on BUSD ###

bnb_market_buy = client.order_market_buy(
    symbol='BNBBUSD',
    quantity=0.037)

### availible bnb limit sell ###

bnb_limit_sell = client.order_limit_sell(
    symbol='BNBBUSD',
    quantity=0.037,
    price=round(float(avg_price_bnb['price']) * round(randbelow(30) * 0.01 + 1.02, 3), 1))

### eth market buy on BUSD ###

eth_market_buy = client.order_market_buy(
    symbol='ETHBUSD',
    quantity=0.0063)

### availible eth limit sell ###

eth_limit_sell = client.order_limit_sell(
    symbol='ETHBUSD',
    quantity=0.0063,
    price=round(float(avg_price_eth['price']) * round(randbelow(30) * 0.01 + 1.02, 3), 2))

### btc market buy on BUSD ###

btc_market_buy = client.order_market_buy(
    symbol='BTCBUSD',
    quantity=0.00051)

### availible btc limit sell ###

btc_limit_sell = client.order_limit_sell(
    symbol='BTCBUSD',
    quantity=0.00051,
    price=round(float(avg_price_btc['price']) * round(randbelow(30) * 0.01 + 1.02, 3), 2))
