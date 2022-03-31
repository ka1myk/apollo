from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

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

BNBBUSDPERP_1h = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR,
)

BNBBUSDPERP_2h = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS,
)

BNBBUSDPERP_4h = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS,
)

BNBBUSDPERP_1d = TA_Handler(
    symbol="BNBBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY,
)


while True:
    if (
        BNBBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and BNBBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and BNBBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and BNBBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and BNBBUSDPERP_1h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and BNBBUSDPERP_2h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and BNBBUSDPERP_4h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and BNBBUSDPERP_1d.get_analysis().summary["RECOMMENDATION"]
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
        time.sleep(45)
        l.kill()
    else:
        w = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "BNBBUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        w.wait()
