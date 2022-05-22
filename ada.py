from tradingview_ta import TA_Handler, Interval, Exchange
from binance.client import Client
import requests, json, time
with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

ADABUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

ADABUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

ADABUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

ADABUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

ADABUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="ADABUSDPERP",
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

        if (
                (
                        ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                )

                or

                (
                        ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                )

        ):
            time.sleep(time_to_wait_one_more_check)

            if (

                    (
                            ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                    )

                    or

                    (
                            ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                    )

            ):
                client.futures_create_order(symbol='ADABUSD', side='BUY', positionSide='LONG', type='MARKET', quantity=10)
                client.futures_create_order(symbol='ADABUSD', side='SELL', positionSide='SHORT', type='MARKET', quantity=10)
                time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
