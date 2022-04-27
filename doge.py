from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order
import subprocess
import time

DOGEBUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

DOGEBUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

DOGEBUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

DOGEBUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

DOGEBUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

DOGEBUSDPERP_INTERVAL_2_HOURS = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS
)

DOGEBUSDPERP_INTERVAL_4_HOURS = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS
)

DOGEBUSDPERP_INTERVAL_1_DAY = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY
)

while True:
    try:
        gs_order = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "DOGEBUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
                "-sm",
                "gs"
            ]
        )
        time.sleep(time_to_create_gs_order)
        gs_order.terminate()

        if (
                DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and DOGEBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and DOGEBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and DOGEBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY")
                    and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY")
                    and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY")
                    and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY")
                    and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and DOGEBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and DOGEBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
                    and DOGEBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_BUY", "BUY")
            ):
                short_order = subprocess.Popen(
                    [
                        "python3",
                        "passivbot.py",
                        "binance_01",
                        "DOGEBUSD",
                        "/root/passivbot_configs/long.json",
                        "-lm",
                        "m",
                        "-sm",
                        "n"
                    ]
                )
                time.sleep(time_to_create_order)
                short_order.terminate()
                time.sleep(time_to_cool_down)

        if (
                DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and DOGEBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and DOGEBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and DOGEBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
        ):
            time.sleep(time_to_wait_one_more_check)

            if (
                    DOGEBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL")
                    and DOGEBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL")
                    and DOGEBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL")
                    and DOGEBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL")
                    and DOGEBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and DOGEBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and DOGEBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
                    and DOGEBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                    in ("STRONG_SELL", "SELL")
            ):
                long_order = subprocess.Popen(
                    [
                        "python3",
                        "passivbot.py",
                        "binance_01",
                        "DOGEBUSD",
                        "/root/passivbot_configs/long.json",
                        "-lm",
                        "n",
                        "-sm",
                        "m"
                    ]
                )
                time.sleep(time_to_create_order)
                long_order.terminate()
                time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
