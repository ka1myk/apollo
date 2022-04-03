from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_creating_order
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
            in ("STRONG_BUY", "BUY")
            and SOLBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and SOLBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and SOLBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):
        l = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "SOLBUSD",
                "/root/passivbot_configs/long.json",
            ]
        )
        time.sleep(time_to_creating_order)
        l.terminate()
