import json
import math
import time

from binance.client import Client
from tradingview_ta import TA_Handler, Interval

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

symbol = 'BTCBUSD'
info = client.futures_exchange_info()


def get_precision(pair):
    for x in info['symbols']:
        if x['symbol'] == pair:
            return x['quantityPrecision']


def round_up(n, decimals=0):
    round_up_multiplier = 10 ** decimals
    return math.ceil(n * round_up_multiplier) / round_up_multiplier


quantityPrecision = get_precision(symbol)
minNotional = round_up(5 / float(client.futures_mark_price(symbol=symbol)["markPrice"]), get_precision(symbol))


INTERVAL_1_MINUTE = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

INTERVAL_5_MINUTES = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

INTERVAL_15_MINUTES = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

INTERVAL_30_MINUTES = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

INTERVAL_1_HOUR = TA_Handler(
    symbol=symbol,
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

while True:
    try:

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        time_to_cool_down = variables['time_to_cool_down']
        multiplier = variables['multiplier']

        quantity = round(minNotional * multiplier, quantityPrecision)

        if (
                INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
        ):
            client.futures_create_order(symbol=symbol,
                                        quantity=quantity,
                                        side='BUY',
                                        positionSide='LONG',
                                        type='MARKET')
            time.sleep(time_to_cool_down)

        if (
                INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
        ):
            client.futures_create_order(symbol=symbol,
                                        quantity=quantity,
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='MARKET')

            time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
