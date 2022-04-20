from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down
import subprocess
import time

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

XRPBUSDPERP_INTERVAL_2_HOURS = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS
)

XRPBUSDPERP_INTERVAL_4_HOURS = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS
)

XRPBUSDPERP_INTERVAL_1_DAY = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY
)

while True:

    gs_order = subprocess.Popen(
        [
            "python3",
            "passivbot.py",
            "binance_01",
            "XRPBUSD",
            "/root/passivbot_configs/long.json",
            "-lm",
            "gs",
            "-sm",
            "gs"
        ]
    )

    if (
            XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and XRPBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and XRPBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and XRPBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):
            gs_order.kill()
            short_order = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "XRPBUSD",
                    "/root/passivbot_configs/long.json",
                    "-lm",
                    "m",
                    "-sm",
                    "n"
                ]
            )
            time.sleep(time_to_create_order)
            short_order.kill()
            time.sleep(time_to_cool_down)

    if (
            XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and XRPBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and XRPBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and XRPBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                XRPBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and XRPBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and XRPBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and XRPBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and XRPBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and XRPBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and XRPBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and XRPBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
        ):
            gs_order.kill()
            long_order = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "XRPBUSD",
                    "/root/passivbot_configs/long.json",
                    "-lm",
                    "n",
                    "-sm",
                    "m"
                ]
            )
            time.sleep(time_to_create_order)
            long_order.kill()
            time.sleep(time_to_cool_down)
