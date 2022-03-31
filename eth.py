from tradingview_ta import TA_Handler, Interval, Exchange
import time
import subprocess

ETHBUSDPERP_1m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE,
)

ETHBUSDPERP_5m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES,
)

ETHBUSDPERP_15m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES,
)

ETHBUSDPERP_30m = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES,
)

ETHBUSDPERP_1h = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR,
)

ETHBUSDPERP_2h = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_2_HOURS,
)

ETHBUSDPERP_4h = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_4_HOURS,
)

ETHBUSDPERP_1d = TA_Handler(
    symbol="ETHBUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY,
)


while True:
    if (
        ETHBUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and ETHBUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and ETHBUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and ETHBUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY")
        and ETHBUSDPERP_1h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ETHBUSDPERP_2h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ETHBUSDPERP_4h.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
        and ETHBUSDPERP_1d.get_analysis().summary["RECOMMENDATION"]
        in ("STRONG_BUY", "BUY")
    ):

        l = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "ETHBUSD",
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
                "ETHBUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        w.wait()
