from binance.client import Client
import json
with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:

        with open('/root/binance_strategies/variables.json') as v:
            variables = json.load(v)

        withdrawAvailable = float(client.futures_account_balance()[9]["withdrawAvailable"])
        balance = float(client.futures_account_balance()[9]["balance"])
        ratio = withdrawAvailable / balance

        # Read in the file
        with open('/root/binance_strategies/variables.json', 'r') as f:
            data = f.read()
        d = json.loads(data)

        if 1 > ratio > 0.80 and d['time_to_cool_down'] != 100:
            d['time_to_cool_down'] = 60

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.79 > ratio > 0.60 and d['time_to_cool_down'] != 300:
            d['time_to_cool_down'] = 120

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.59 > ratio > 0.40 and d['time_to_cool_down'] != 600:
            d['time_to_cool_down'] = 540

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

        if 0.40 > ratio and d['time_to_cool_down'] != 43200:
            d['time_to_cool_down'] = 43200

            with open('/root/binance_strategies/variables.json', 'w') as f:
                json.dump(d, f)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")