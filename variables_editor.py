from binance.client import Client
import json

with open('/root/binance_strategies/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        withdrawAvailable = float(client.futures_account_balance()[9]["withdrawAvailable"])
        balance = float(client.futures_account_balance()[9]["balance"])
        ratio = withdrawAvailable / balance

        with open('/root/binance_strategies/variables.json', 'r') as f:
            data = f.read()
        d = json.loads(data)

        if (1 > ratio > 0.95) and d['time_to_cool_down'] != 60 and d['multiplier'] != 1:
            d['time_to_cool_down'] = 60
            d['multiplier'] = 1

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if (0.94 > ratio > 0.90) and d['time_to_cool_down'] != 300 and d['multiplier'] != 1:
            d['time_to_cool_down'] = 300
            d['multiplier'] = 1

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if (0.89 > ratio > 0.80) and d['time_to_cool_down'] != 600 and d['multiplier'] != 1:
            d['time_to_cool_down'] = 600
            d['multiplier'] = 1

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if (0.79 > ratio > 0.70) and d['time_to_cool_down'] != 1200 and d['multiplier'] != 1:
            d['time_to_cool_down'] = 1200
            d['multiplier'] = 1

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if (0.69 > ratio > 0.50) and d['time_to_cool_down'] != 3000 and d['multiplier'] != 1:
            d['time_to_cool_down'] = 3000
            d['multiplier'] = 1

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if (0.49 > ratio) and d['time_to_cool_down'] != 6000 and d['multiplier'] != 1:
            d['time_to_cool_down'] = 6000
            d['multiplier'] = 1

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")