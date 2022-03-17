from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

DOGEBUSDPERP_1m = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

DOGEBUSDPERP_5m = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

DOGEBUSDPERP_15m = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

DOGEBUSDPERP_30m = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

DOGEBUSDPERP_1h = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR,
)

DOGEBUSDPERP_2h = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS,
)

DOGEBUSDPERP_4h = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS,
)

DOGEBUSDPERP_1d = TA_Handler(
    symbol="DOGEBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY,
)


while True:
    if (
        DOGEBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"] 
        in ("STRONG_BUY", "BUY")
        and DOGEBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and DOGEBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and DOGEBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and DOGEBUSDPERP_1h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and DOGEBUSDPERP_2h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and DOGEBUSDPERP_1d.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and DOGEBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
    ):

        l = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "DOGEBUSD",
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
                "DOGEBUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        time.sleep(45)
        w.terminate()
