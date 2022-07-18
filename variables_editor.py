import json
import time
from datetime import datetime
from binance.client import Client

# with open('/root/passivbot/api-keys.json') as p:
with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:
        timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")

        # with open('/root/apollo/variables.json', 'r') as f:
        with open('variables.json', 'r') as f:
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

        if 1 > ratio > 0.98:
            d['time_to_cool_down'] = round(60 / coins_amount)

        if 0.97 > ratio > 0.95:
            d['time_to_cool_down'] = round(180 / coins_amount)

        if 0.94 > ratio > 0.90:
            d['time_to_cool_down'] = round(300 / coins_amount)

        if 0.89 > ratio > 0.80:
            d['time_to_cool_down'] = round(900 / coins_amount)

        if 0.79 > ratio > 0.70:
            d['time_to_cool_down'] = round(1800 / coins_amount)

        if 0.69 > ratio > 0.60:
            d['time_to_cool_down'] = round(3600 / coins_amount)

        if 0.59 > ratio > 0.50:
            d['time_to_cool_down'] = round(7200 / coins_amount)

        if 0.49 > ratio > 0.40:
            d['time_to_cool_down'] = round(14400 / coins_amount)

        if 0.39 > ratio > 0.30:
            d['time_to_cool_down'] = round(21600 / coins_amount)

        if 0.29 > ratio > 0.20:
            d['time_to_cool_down'] = round(28800 / coins_amount)

        if 0.19 > ratio:
            d['time_to_cool_down'] = round(57600 / coins_amount)

        # with open('/root/apollo/variables.json', 'w') as f:
        with open('variables.json', 'w') as f:
            json.dump(d, f)

        time.sleep(exception_cool_down)
    except Exception as e:
        print(timestamp, "Function errored out!", e)
        time.sleep(exception_cool_down)