#!/usr/bin/python
# -*- coding: utf-8 -*-
# ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

import urllib.request
import json
import time
import subprocess
from variables import rsi_obv_delta, time_to_work

while True:

    with urllib.request.urlopen(
        "http://10.16.0.1:5000/indicators?exchange=binance&symbol=FTTBUSD&interval=1m"
    ) as url:
        data1m = json.loads(url.read().decode())
        rsi_obv_1m = data1m["rsi_obv"]

    with urllib.request.urlopen(
        "http://10.16.0.1:5000/indicators?exchange=binance&symbol=FTTBUSD&interval=3m"
    ) as url:
        data3m = json.loads(url.read().decode())
        rsi_obv_3m = data3m["rsi_obv"]

    with urllib.request.urlopen(
        "http://10.16.0.1:5000/indicators?exchange=binance&symbol=FTTBUSD&interval=5m"
    ) as url:
        data5m = json.loads(url.read().decode())
        rsi_obv_5m = data5m["rsi_obv"]
    with urllib.request.urlopen(
        "http://10.16.0.1:5000/indicators?exchange=binance&symbol=FTTBUSD&interval=15m"
    ) as url:
        data15m = json.loads(url.read().decode())
        rsi_obv_15m = data15m["rsi_obv"]

    average_rsi_obv = (rsi_obv_1m + rsi_obv_3m + rsi_obv_5m + rsi_obv_15m) / 4
    if (
        abs(rsi_obv_1m - average_rsi_obv) < rsi_obv_delta
        and abs(rsi_obv_3m - average_rsi_obv) < rsi_obv_delta
        and abs(rsi_obv_5m - average_rsi_obv) < rsi_obv_delta
        and abs(rsi_obv_15m - average_rsi_obv) < rsi_obv_delta
    ):

        l = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "FTTBUSD",
                "/root/passivbot_configs/long.json",
            ]
        )

        time.sleep(time_to_work)
        l.terminate()
    else:
        w = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "FTTBUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
            ]
        )
        time.sleep(time_to_work)
        l.terminate()
