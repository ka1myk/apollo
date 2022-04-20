from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check
import subprocess
import time

SOLBUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

SOLBUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

SOLBUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

SOLBUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

SOLBUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

SOLBUSDPERP_INTERVAL_2_HOURS = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS
)

SOLBUSDPERP_INTERVAL_4_HOURS = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS
)

SOLBUSDPERP_INTERVAL_1_DAY = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY
)

while True:

    if (
            SOLBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and SOLBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and SOLBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and SOLBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and SOLBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and SOLBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and SOLBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and SOLBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                SOLBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and SOLBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and SOLBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and SOLBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and SOLBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and SOLBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and SOLBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and SOLBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):
            short_order = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "SOLBUSD",
                    "/root/passivbot_configs/long.json",
                    "-lm",
                    "m",
                    "-sm",
                    "n"
                ]
            )
            time.sleep(time_to_create_order)
            short_order.kill()

    if (
            SOLBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and SOLBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and SOLBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and SOLBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and SOLBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and SOLBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and SOLBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and SOLBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                SOLBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and SOLBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and SOLBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and SOLBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and SOLBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and SOLBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and SOLBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and SOLBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
        ):
            long_order = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "SOLBUSD",
                    "/root/passivbot_configs/long.json",
                    "-lm",
                    "n",
                    "-sm",
                    "m"
                ]
            )
            time.sleep(time_to_create_order)
            long_order.kill()
