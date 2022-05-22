from tradingview_ta import TA_Handler, Interval, Exchange
from binance.client import Client
import requests, json, time

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

GMTBUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="GMTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

GMTBUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="GMTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

GMTBUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="GMTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

GMTBUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="GMTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

GMTBUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="GMTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

while True:

    try:

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)
        time_to_cool_down = variables['time_to_cool_down']

        if (
                (
                        GMTBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and GMTBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and GMTBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and GMTBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and GMTBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                )

                or

                (
                        GMTBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and GMTBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and GMTBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and GMTBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and GMTBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                )

        ):
            client.futures_create_order(symbol='GMTBUSD', side='BUY', positionSide='LONG', type='MARKET', quantity=3.7)
            client.futures_create_order(symbol='GMTBUSD', side='SELL', positionSide='SHORT', type='MARKET', quantity=3.7)
            time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
