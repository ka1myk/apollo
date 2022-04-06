from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check
import subprocess
import time

ETHBUSDPERP_1m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

ETHBUSDPERP_5m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

ETHBUSDPERP_15m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

ETHBUSDPERP_30m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

while True:
    if (
            ETHBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and ETHBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and ETHBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
            and ETHBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                ETHBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and ETHBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and ETHBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
                and ETHBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY")
        ):
            l = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "ETHBUSD",
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
            ETHBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and ETHBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and ETHBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
            and ETHBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_SELL")
    ):
        time.sleep(time_to_wait_one_more_check)

        if (
                ETHBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and ETHBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and ETHBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
                and ETHBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_SELL")
        ):
            s = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "ETHBUSD",
                    "/root/passivbot_configs/long.json",
                    "-lm",
                    "m",
                    "-sm",
                    "n"
                ]
            )
            time.sleep(time_to_create_order)
            s.terminate()
