from tradingview_ta import TA_Handler, Interval, Exchange
from binance.client import Client
from secrets import randbelow
import requests, json, time

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:

    try:
        with open('/root/passivbot_configs/variables.json') as v:
            variables = json.load(v)
        time_to_cool_down = variables['time_to_cool_down']

        if randbelow(2) == 1:
            client.futures_create_order(symbol='BTCBUSD', side='BUY', positionSide='LONG', type='MARKET', quantity=0.001)
        else:
            client.futures_create_order(symbol='BTCBUSD', side='SELL', positionSide='SHORT', type='MARKET', quantity=0.001)

        time.sleep(time_to_cool_down*4)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
