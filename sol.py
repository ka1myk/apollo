from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

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

SOLBUSDPERP_1h = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR,
)

SOLBUSDPERP_2h = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS,
)

SOLBUSDPERP_4h = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS,
)

SOLBUSDPERP_1d = TA_Handler(
    symbol="SOLBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY,
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
        and SOLBUSDPERP_1h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and SOLBUSDPERP_2h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and SOLBUSDPERP_1d.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and SOLBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
    ):

        l = subprocess.Popen(
            [
                "python3",
                "passivbot/passivbot.py",
                "binance",
                "SOLBUSD",
                "passivbot_configs/long.json",
            ]
        )
        time.sleep(45)
        l.terminate()
    else:
        w = subprocess.Popen(
            [
                "python3",
                "passivbot/passivbot.py",
                "binance",
                "SOLBUSD",
                "passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        time.sleep(45)
        w.terminate()
