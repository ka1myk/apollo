from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check
import subprocess
import time

ADABUSDPERP_1m = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

ADABUSDPERP_5m = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

ADABUSDPERP_15m = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

ADABUSDPERP_30m = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

while True:
    if (
            ADABUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and ADABUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and ADABUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and ADABUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                ADABUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and ADABUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and ADABUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and ADABUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
        ):
            l = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "ADABUSD",
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
            ADABUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and ADABUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and ADABUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and ADABUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                ADABUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and ADABUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and ADABUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and ADABUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
        ):
            s = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "ADABUSD",
                    "/root/passivbot_configs/long.json",
                    "-lm",
                    "m",
                    "-sm",
                    "n"
                ]
            )
            time.sleep(time_to_create_order)
            s.terminate()
