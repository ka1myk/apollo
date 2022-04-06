from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check
import subprocess
import time

SOLBUSDPERP_1m = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

SOLBUSDPERP_5m = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

SOLBUSDPERP_15m = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

SOLBUSDPERP_30m = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

while True:
    if (
            SOLBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and SOLBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and SOLBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and SOLBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                SOLBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and SOLBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and SOLBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and SOLBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
        ):
            l = subprocess.Popen(
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
            l.terminate()

    if (
            SOLBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and SOLBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and SOLBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and SOLBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                SOLBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and SOLBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and SOLBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and SOLBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
        ):
            s = subprocess.Popen(
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
            s.terminate()
