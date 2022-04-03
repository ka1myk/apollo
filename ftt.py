from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_creating_order
import subprocess
import time

FTTBUSDPERP_1m = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

FTTBUSDPERP_5m = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

FTTBUSDPERP_15m = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

FTTBUSDPERP_30m = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

while True:
    if (
            FTTBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and FTTBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and FTTBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and FTTBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):
        l = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "FTTBUSD",
                "/root/passivbot_configs/long.json",
            ]
        )
        time.sleep(time_to_creating_order)
        l.terminate()
