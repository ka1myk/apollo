import math
import json
import time
from datetime import datetime
from binance.client import Client
from tradingview_ta import TA_Handler, Interval

with open('/root/binance_strategies/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

symbol = 'NEARBUSD'
info = client.futures_exchange_info()


def get_precision(pair):
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


quantityPrecision = get_precision(symbol)
minNotional = round_up(float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
                       get_precision(symbol))

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
        timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        time_to_wait_one_more_check = variables['time_to_wait_one_more_check']
        exception_cool_down = variables['exception_cool_down']
        time_to_cool_down = variables['time_to_cool_down']

        multiplier = variables['multiplier']

        tradingview_open_long_signal = variables['tradingview_open_long_signal']
        tradingview_open_short_signal = variables['tradingview_open_short_signal']

        quantity = round(minNotional * multiplier, quantityPrecision)

        if (
                INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in set(tradingview_open_long_signal)
                and INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in set(tradingview_open_long_signal)
                and INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in set(tradingview_open_long_signal)
                and INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in set(tradingview_open_long_signal)
                and INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in set(tradingview_open_long_signal)
        ):
            client.futures_create_order(symbol=symbol,
                                        quantity=quantity,
                                        side='SELL',
                                        positionSide='SHORT',
                                        type='MARKET')
            print(timestamp, symbol, 'open short and wait', time_to_cool_down)
            time.sleep(time_to_cool_down)

        if (
                INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in tradingview_open_short_signal
                and INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in tradingview_open_short_signal
                and INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in tradingview_open_short_signal
                and INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in tradingview_open_short_signal
                and INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in tradingview_open_short_signal
        ):
            client.futures_create_order(symbol=symbol,
                                        quantity=quantity,
                                        side='BUY',
                                        positionSide='LONG',
                                        type='MARKET')
            print(timestamp, symbol, 'open long and wait', time_to_cool_down)
            time.sleep(time_to_cool_down)

    except Exception as e:
        print(timestamp, "Function errored out!", e)
        time.sleep(exception_cool_down)
