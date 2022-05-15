import requests, json
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order
import subprocess
import time

headers = {'coinglassSecret': '50f90ddcd6a8437992431ab0f1b698c1'}




while True:
    try:
        
        url = requests.get("https://open-api.coinglass.com/api/pro/v1/futures/liquidation/detail/chart?symbol=ETH&timeType=10", headers=headers)
        text = url.text
        data = json.loads(text)
        
        gs_order = subprocess.Popen(
            [
                "python3",
                "passivbot.py",
                "binance_01",
                "ETHBUSD",
                "/root/passivbot_configs/long.json",
                "-lm",
                "gs",
                "-sm",
                "gs"
            ]
        )
        time.sleep(time_to_create_gs_order)
        gs_order.terminate()

        long_signal = data['data'][90]['buyVolUsd']
        if long_signal > 1000000:

            long_order = subprocess.Popen(
                [
                    "python3",
                    "passivbot.py",
                    "binance_01",
                    "ETHBUSD",
                    "/root/passivbot_configs/long.json",
                    "-lm",
                    "n",
                    "-sm",
                    "m"
                ]
            )
            time.sleep(time_to_create_order)
            long_order.terminate()
            time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
