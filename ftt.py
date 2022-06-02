from binance.client import Client
from secrets import randbelow
import json, time

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:

    try:
        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        time_to_cool_down = variables['time_to_cool_down']
        leverage = variables['leverage']
        multiplier = variables['multiplier']

        symbol = 'FTTBUSD'
        quantityPrecision = 3
        minNotional = 0.2
        quantity = round(minNotional * multiplier, quantityPrecision)

        if randbelow(2) == 1:
            client.futures_create_order(symbol=symbol,
                                        side='BUY',
                                        positionSide='LONG',
                                        type='MARKET',
                                        quantity=quantity)
        else:
            client.futures_create_order(symbol=symbol,
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='MARKET',
                                        quantity=quantity)

        time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")