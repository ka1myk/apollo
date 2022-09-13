import json
from binance.client import Client
from notify import send_to_telegram
import platform


try:
    with open('variables.json') as v:
        variables = json.load(v)

    with open('api-keys.json') as p:
        creds = json.load(p)
    client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

    currency = variables['currency']

    # coins = ["ADA", "BNB", "BTC", "DOT", "ETH", "SOL", "XRP"]
    coins = ["XRP"]
    for x in coins:
        symbol = x + currency1

    # market_buy = client.order_market_buy(
    #     symbol= coin + currency,
    #     quantity=min_quantity)
    # limit_sell = client.order_limit_sell(
    #     symbol= coin + currency,
    #     quantity=min_quantity,
    #     price=round(float(avg_price['price']) * round(randbelow(30) * 0.01 + 1.02, 3), 1))
except Exception as message:
    print(send_to_telegram(str(platform.node()) + str(message)))
