from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

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

ADABUSDPERP_1h = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR,
)

ADABUSDPERP_2h = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS,
)

ADABUSDPERP_4h = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS,
)

ADABUSDPERP_1d = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY,
)


while True:
    if (
        ADABUSDPERP_1m.get_analysis().summary["RECOMMENDATION"] 
        in ("STRONG_BUY", "BUY")
        and ADABUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ADABUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ADABUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ADABUSDPERP_1h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ADABUSDPERP_2h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ADABUSDPERP_1d.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ADABUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
    ):

        l = subprocess.Popen(
            [
                "python3",
                "passivbot/passivbot.py",
                "binance",
                "ADABUSD",
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
                "ADABUSD",
                "passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        time.sleep(45)
        w.terminate()
