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

        multiplier = d['multiplier']
        exception_cool_down = d['exception_cool_down']
        qty_coins_liquidation = d['qty_coins_liquidation']
        tradingview_open_long_signal = d['tradingview_open_long_signal']
        tradingview_open_short_signal = d['tradingview_open_short_signal']

        totalMarginBalance = round(float(client.futures_account()['totalMarginBalance']), 3)
        totalWalletBalance = round(float(client.futures_account()['totalWalletBalance']), 3)

        ratio = round(float(totalMarginBalance / totalWalletBalance), 3)

        print(timestamp, "totalMarginBalance", totalMarginBalance,
              "totalWalletBalance", totalWalletBalance,
              "time_to_cool_down", d['time_to_cool_down'],
              'multiplier', d['multiplier'],
              "ratio", ratio,
              tradingview_open_long_signal,
              tradingview_open_short_signal)

        if 1 > ratio > 0.98:
            d['multiplier'] = 1
            d['time_to_cool_down'] = 300
            d['qty_coins_liquidation'] = 350
            d['tradingview_open_long_signal'] = ["STRONG_BUY", "BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL", "SELL"]

        if 0.97 > ratio > 0.95:
            d['multiplier'] = 2
            d['time_to_cool_down'] = 600
            d['qty_coins_liquidation'] = 400
            d['tradingview_open_long_signal'] = ["STRONG_BUY", "BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL", "SELL"]

        if 0.94 > ratio > 0.90:
            d['multiplier'] = 3
            d['time_to_cool_down'] = 1200
            d['qty_coins_liquidation'] = 450
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

        if 0.89 > ratio > 0.80:
            d['multiplier'] = 4
            d['time_to_cool_down'] = 2400
            d['qty_coins_liquidation'] = 500
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

        if 0.79 > ratio > 0.70:
            d['multiplier'] = 5
            d['time_to_cool_down'] = 4800
            d['qty_coins_liquidation'] = 550
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

        if 0.69 > ratio:
            d['multiplier'] = 6
            d['time_to_cool_down'] = 9600
            d['qty_coins_liquidation'] = 600
            d['tradingview_open_long_signal'] = ["STRONG_BUY"]
            d['tradingview_open_short_signal'] = ["STRONG_SELL"]

        with open('/root/binance_strategies/variables.json', 'w') as f:
            json.dump(d, f)

    except Exception as e:
        print(timestamp, "Function errored out!", e)
        time.sleep(exception_cool_down)