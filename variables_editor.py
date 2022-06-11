import json
import time
from datetime import datetime
from binance.client import Client

with open('/root/binance_strategies/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:
        timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")

        with open('/root/binance_strategies/variables.json', 'r') as f:
            data = f.read()

        d = json.loads(data)

        exception_cool_down = d['exception_cool_down']
        multiplier = d['multiplier']
        tradingview_open_long_signal = d['tradingview_open_long_signal']
        tradingview_open_short_signal = d['tradingview_open_short_signal']

        withdrawAvailable = round(float(client.futures_account_balance()[9]["withdrawAvailable"]), 2)
        balance = round(float(client.futures_account_balance()[9]["balance"]), 2)
        ratio = round(float(withdrawAvailable / balance), 2)

        print(timestamp, "withdrawAvailable", withdrawAvailable, "balance", balance, "time_to_cool_down",
              d['time_to_cool_down'], 'multiplier', d['multiplier'], "ratio", ratio, tradingview_open_long_signal,
              tradingview_open_short_signal)

        if 1 > ratio > 0.95:
            d['multiplier'] = 1
            d['time_to_cool_down'] = 60
            d['tradingview_open_long_signal'] = ["STRONG_BUY", "BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL", "SELL"]

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.94 > ratio > 0.90:
            d['multiplier'] = 1
            d['time_to_cool_down'] = 300
            d['tradingview_open_long_signal'] = ["STRONG_BUY", "BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL", "SELL"]

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.89 > ratio > 0.80:
            d['multiplier'] = 1
            d['time_to_cool_down'] = 600
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.79 > ratio > 0.70:
            d['multiplier'] = 1
            d['time_to_cool_down'] = 1200
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.69 > ratio > 0.50:
            d['multiplier'] = 1
            d['time_to_cool_down'] = 3000
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.49 > ratio:
            d['multiplier'] = 1
            d['time_to_cool_down'] = 6000
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

    except Exception as e:
        print(timestamp, "Function errored out!", e)
        time.sleep(exception_cool_down)
