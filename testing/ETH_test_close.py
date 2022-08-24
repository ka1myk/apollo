import math
import json
from datetime import datetime
from binance.client import Client

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

symbol = 'ETHBUSD'
greed = 1
multiplier = 1.3
long_profit_percentage = 1.01
short_profit_percentage = 0.99

info = client.futures_exchange_info()


def get_pricePrecision(pair):
    for x in info['symbols']:
        if x['symbol'] == pair:
            return x['pricePrecision']


def get_quantityPrecision(pair):
    for x in info['symbols']:
        if x['symbol'] == pair:
            return x['quantityPrecision']


def get_notional(pair):
    for x in info['symbols']:
        if x['symbol'] == pair:
            for y in x['filters']:
                if y['filterType'] == 'MIN_NOTIONAL':
                    return y['notional']


def round_up(n, decimals=0):
    round_up_multiplier = 10 ** decimals
    return math.ceil(n * round_up_multiplier) / round_up_multiplier


timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")

quantityPrecision = get_quantityPrecision(symbol)
pricePrecision = get_pricePrecision(symbol)
minNotional = round_up(float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
                       get_quantityPrecision(symbol))
creatingQuantity = round(minNotional * multiplier * greed, quantityPrecision)

#####################################################
client.futures_create_order(symbol=symbol,
                            quantity=creatingQuantity,
                            side='BUY',
                            positionSide='LONG',
                            type='MARKET')

client.futures_create_order(symbol=symbol,
                            quantity=creatingQuantity,
                            side='SELL',
                            positionSide='SHORT',
                            type='MARKET')
#####################################################

long_positionAmt = abs(float(client.futures_position_information(symbol=symbol)[1]["positionAmt"]))
long_take_profit_price = round_up(
    float(client.futures_position_information(symbol=symbol)[1]["entryPrice"]) * long_profit_percentage,
    get_pricePrecision(symbol))

short_positionAmt = abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]))
short_take_profit_price = round_up(
    float(client.futures_position_information(symbol=symbol)[2]["entryPrice"]) * short_profit_percentage,
    get_pricePrecision(symbol))

print(timestamp)
print("long_entryPrice", client.futures_position_information(symbol=symbol)[1]["entryPrice"])
print("short_entryPrice", client.futures_position_information(symbol=symbol)[2]["entryPrice"])
print("long_positionAmt", long_positionAmt, "long_take_profit_price", long_take_profit_price)
print("short_positionAmt", short_positionAmt, "short_take_profit_price", short_take_profit_price)

client.futures_cancel_all_open_orders(symbol=symbol)

if float(long_positionAmt) != 0:
    client.futures_create_order(symbol=symbol,
                                quantity=round(long_positionAmt * 0.7, quantityPrecision),
                                price=round(long_take_profit_price * 1, pricePrecision),
                                side='SELL',
                                positionSide='LONG',
                                type='LIMIT',
                                timeInForce="GTC"
                                )

    client.futures_create_order(symbol=symbol,
                                quantity=round(long_positionAmt * 0.15, quantityPrecision),
                                price=round(long_take_profit_price * 1.01, pricePrecision),
                                side='SELL',
                                positionSide='LONG',
                                type='LIMIT',
                                timeInForce="GTC"
                                )

    client.futures_create_order(symbol=symbol,
                                quantity=round(long_positionAmt * 0.15, quantityPrecision),
                                price=round(long_take_profit_price * 1.02, pricePrecision),
                                side='SELL',
                                positionSide='LONG',
                                type='LIMIT',
                                timeInForce="GTC"
                                )

if float(short_positionAmt) != 0:
    client.futures_create_order(symbol=symbol,
                                quantity=round(short_positionAmt * 0.7, quantityPrecision),
                                price=round(short_take_profit_price * 1, pricePrecision),
                                side='BUY',
                                positionSide='SHORT',
                                type='LIMIT',
                                timeInForce="GTC"
                                )

    client.futures_create_order(symbol=symbol,
                                quantity=round(short_positionAmt * 0.15, quantityPrecision),
                                price=round(short_take_profit_price * 0.99, pricePrecision),
                                side='BUY',
                                positionSide='SHORT',
                                type='LIMIT',
                                timeInForce="GTC"
                                )

    client.futures_create_order(symbol=symbol,
                                quantity=round(short_positionAmt * 0.15, quantityPrecision),
                                price=round(short_take_profit_price * 0.98, pricePrecision),
                                side='BUY',
                                positionSide='SHORT',
                                type='LIMIT',
                                timeInForce="GTC"
                                )
