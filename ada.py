#!/usr/bin/python

# ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

from tradingview_ta import TA_Handler, Interval, Exchange
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

while True:
    while (
            ADABUSDPERP_1m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and ADABUSDPERP_5m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and ADABUSDPERP_15m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
            and ADABUSDPERP_30m.get_analysis().summary["RECOMMENDATION"]
            in ("STRONG_BUY", "BUY")
    ):

        try:
            w.kill()
        except Exception as ex:            
            l = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "ADABUSD",
                    "/root/passivbot_configs/long.json",
                ]
            )
    try:
        l.kill()
    except Exception as ex:
        w = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "ADABUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
