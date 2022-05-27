from tradingview_ta import TA_Handler, Interval, Exchange
from binance.client import Client
import requests, json, time

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

XRPBUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

XRPBUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

XRPBUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

XRPBUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

XRPBUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

while True:
    try:

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        time_to_wait_one_more_check = variables['time_to_wait_one_more_check']
        time_to_cool_down = variables['time_to_cool_down']
        leverage = variables['leverage']
        multiplier = variables['multiplier']

        symbol = 'XRPBUSD'
        pricePrecision = 4
        quantityPrecision = 0
        minNotional = 13
        quantity = round(minNotional * multiplier, quantityPrecision)

        if (
                XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
            ):
                client.futures_create_order(symbol=symbol,
                                            side='SELL',
                                            positionSide='SHORT',
                                            type='MARKET',
                                            leverage=leverage,
                                            quantity=quantity)

                time.sleep(time_to_cool_down)

        if (
                XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
            ):
                client.futures_create_order(symbol=symbol,
                                            side='BUY',
                                            positionSide='LONG',
                                            type='MARKET',
                                            leverage=leverage,
                                            quantity=quantity)

                time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
