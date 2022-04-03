#!/usr/bin/python

# ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

from tradingview_ta import TA_Handler, Interval, Exchange
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

while True:

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

    while (
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
