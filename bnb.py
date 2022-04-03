from tradingview_ta import TA_Handler, Interval, Exchange
from variables import time_to_creating_order
import subprocess
import time

BNBBUSDPERP_1m = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

BNBBUSDPERP_5m = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

BNBBUSDPERP_15m = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

BNBBUSDPERP_30m = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

while True:
    if (
            BNBBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and BNBBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and BNBBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and BNBBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):
        l = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "BNBBUSD",
                "/root/passivbot_configs/long.json",
            ]
        )
        time.sleep(time_to_creating_order)
        l.terminate()
