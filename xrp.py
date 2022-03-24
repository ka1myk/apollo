from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

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

XRPBUSDPERP_1h = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR,
)

XRPBUSDPERP_2h = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS,
)

XRPBUSDPERP_4h = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS,
)

XRPBUSDPERP_1d = TA_Handler(
    symbol="XRPBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY,
)


while True:
    if (
        XRPBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"] 
        in ("STRONG_BUY")
        and XRPBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and XRPBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and XRPBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and XRPBUSDPERP_1h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and XRPBUSDPERP_2h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and XRPBUSDPERP_1d.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and XRPBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
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
        time.sleep(45)
        l.terminate()
    else:
        w = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "XRPBUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        time.sleep(45)
        w.terminate()
