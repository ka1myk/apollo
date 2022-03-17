from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

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

FTTBUSDPERP_1h = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR,
)

FTTBUSDPERP_2h = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS,
)

FTTBUSDPERP_4h = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS,
)

FTTBUSDPERP_1d = TA_Handler(
    symbol="FTTBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY,
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
        and FTTBUSDPERP_1h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and FTTBUSDPERP_2h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and FTTBUSDPERP_1d.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and FTTBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
    ):

        l = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance",
                "FTTBUSD",
                "passivbot_configs/long.json",
            ]
        )
        time.sleep(45)
        l.terminate()
    else:
        w = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance",
                "FTTBUSD",
                "passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        time.sleep(45)
        w.terminate()
