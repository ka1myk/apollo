import json
from secrets import randbelow

from binance.client import Client
from binance.helpers import round_step_size

with open('variables.json') as v:
    variables = json.load(v)

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

currency = variables['currency']
greed = variables['greed']

coins = ["ADA", "BNB", "BTC", "DOT", "ETH", "SOL", "XRP"]

for x in coins:
    symbol = x + currency

    info = client.get_symbol_info(symbol)
    price = client.get_avg_price(symbol=symbol)['price']


    def get_notional(symbol):
        for y in info['filters']:
            if y['filterType'] == 'MIN_NOTIONAL':
                return y['minNotional']


    def get_price_precision(symbol):
        n = len(str(get_rounded_price(symbol, price)).split(".")[1])
        return n


    def get_tick_size(symbol):
        for y in info['filters']:
            if y['filterType'] == 'PRICE_FILTER':
                return y['tickSize']


    def get_rounded_price(symbol: str, price: float) -> float:
        return round_step_size(price, get_tick_size(symbol))


    market_buy = client.order_market_buy(symbol=symbol, side='BUY', type='MARKET',
                                         quoteOrderQty=float(get_notional(symbol)))

    avg_price_with_profit_and_precision = round(float(price) * float(randbelow(30) * 0.01 + 1.02),
                                                get_price_precision(symbol))
    executedQty = float(client.get_all_orders(symbol=symbol, limit=1)[0]["executedQty"])

    limit_sell = client.order_limit_sell(symbol=symbol, quantity=executedQty,
                                         price=avg_price_with_profit_and_precision)
