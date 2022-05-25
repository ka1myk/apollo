from binance.client import Client
import json

with open('api-keys.json') as p:
    creds = json.load(p)
client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:

        with open('variables.json') as v:
            variables = json.load(v)

        withdrawAvailable = float(client.futures_account_balance()[9]["withdrawAvailable"])
        balance = float(client.futures_account_balance()[9]["balance"])
        ratio = withdrawAvailable / balance

        # Read in the file
        with open('variables.json', 'r') as f:
            data = f.read()
        d = json.loads(data)

        if (1 > ratio > 0.90) and d['time_to_cool_down'] != 100 and d['multiplier'] != 1:
            d['time_to_cool_down'] = 100
            d['multiplier'] = 1

            with open('variables.json', 'w') as f:
                json.dump(d, f)

        if (0.89 > ratio > 0.76) and d['time_to_cool_down'] != 300 and d['multiplier'] != 1.3:
            d['time_to_cool_down'] = 300
            d['multiplier'] = 1.3

            with open('variables.json', 'w') as f:
                json.dump(d, f)

        if (0.75 > ratio > 0.60) and d['time_to_cool_down'] != 600 and d['multiplier'] != 1.5:
            d['time_to_cool_down'] = 600
            d['multiplier'] = 1.5

            with open('variables.json', 'w') as f:
                json.dump(d, f)

        if (0.59 > ratio) and d['time_to_cool_down'] != 43200 and d['multiplier'] != 2:
            d['time_to_cool_down'] = 43200
            d['multiplier'] = 2

            with open('variables.json', 'w') as f:
                json.dump(d, f)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
