import json
import time
from datetime import datetime
from binance.client import Client

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:
        timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")

        with open('/root/apollo/variables.json', 'r') as f:
            data = f.read()

        d = json.loads(data)

        exception_cool_down = d['exception_cool_down']
        coins = d['coins']

        totalMarginBalance = round(float(client.futures_account()['totalMarginBalance']), 3)
        totalWalletBalance = round(float(client.futures_account()['totalWalletBalance']), 3)
        ratio = round(float(totalMarginBalance / totalWalletBalance), 3)
        coins_amount = len(coins)

        print(timestamp, "totalMarginBalance", totalMarginBalance,
              "totalWalletBalance", totalWalletBalance,
              "time_to_cool_down", d['time_to_cool_down'],
              'multiplier', d['multiplier'],
              "ratio", ratio,
              "coins_amount", coins_amount)

        #Fibonacci numbers
        #delta ratio 1, 2, 3, 5, 8, 13, 21, 34, 55

        if 1 > ratio > 0.99:
            d['time_to_cool_down'] = round(60 / coins_amount)

        if 0.99 > ratio > 0.97:
            d['time_to_cool_down'] = round(180 / coins_amount)

        if 0.97 > ratio > 0.94:
            d['time_to_cool_down'] = round(300 / coins_amount)

        if 0.94 > ratio > 0.89:
            d['time_to_cool_down'] = round(900 / coins_amount)

        if 0.89 > ratio > 0.81:
            d['time_to_cool_down'] = round(1800 / coins_amount)

        if 0.81 > ratio > 0.68:
            d['time_to_cool_down'] = round(3600 / coins_amount)

        if 0.68 > ratio > 0.47:
            d['time_to_cool_down'] = round(7200 / coins_amount)

        if 0.47 > ratio > 0.13:
            d['time_to_cool_down'] = round(14400 / coins_amount)

        if 0.13 > ratio:
            d['time_to_cool_down'] = round(21600 / coins_amount)

        with open('/root/apollo/variables.json', 'w') as f:
            json.dump(d, f)

        time.sleep(exception_cool_down)
    except Exception as e:
        print(timestamp, "Function errored out!", e)
        time.sleep(exception_cool_down)
