from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_create_order, time_to_wait_one_more_check
import subprocess
import time

XRPBUSDPERP_1m = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

XRPBUSDPERP_5m = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

XRPBUSDPERP_15m = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

XRPBUSDPERP_30m = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

while True:
    if (
            XRPBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and XRPBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and XRPBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and XRPBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):
        time.sleep(time_to_wait_one_more_check)
        
        if (
                XRPBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
                and XRPBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
                in ("STRONG_BUY", "BUY")
        ):
            l = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "XRPBUSD",
                    "/root/passivbot_configs/long.json",
                ]
            )
            time.sleep(time_to_create_order)
            l.terminate()
