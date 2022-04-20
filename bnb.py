from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order
import subprocess
import time

BNBBUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

BNBBUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

BNBBUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

BNBBUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

BNBBUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

BNBBUSDPERP_INTERVAL_2_HOURS = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS
)

BNBBUSDPERP_INTERVAL_4_HOURS = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS
)

BNBBUSDPERP_INTERVAL_1_DAY = TA_Handler(
    symbol="BNBBUSDPERP",
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
            "BNBBUSD",
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
            BNBBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and BNBBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and BNBBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and BNBBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and BNBBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and BNBBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and BNBBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and BNBBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                BNBBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and BNBBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and BNBBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and BNBBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and BNBBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and BNBBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and BNBBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and BNBBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):

            short_order = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "BNBBUSD",
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
            BNBBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and BNBBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and BNBBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and BNBBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and BNBBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and BNBBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and BNBBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
            and BNBBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL", "SELL")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                BNBBUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and BNBBUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and BNBBUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and BNBBUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and BNBBUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and BNBBUSDPERP_INTERVAL_2_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and BNBBUSDPERP_INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
                and BNBBUSDPERP_INTERVAL_1_DAY.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL", "SELL")
        ):

            long_order = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "BNBBUSD",
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
