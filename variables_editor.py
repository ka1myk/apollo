from binance.client import Client
import time
import json
import subprocess

with open('/root/passivbot_configs/variables.json') as v:
    variables = json.load(v)

time_to_wait_one_more_check = variables['time_to_wait_one_more_check']

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)

client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])
while True:
    try:

        eth = subprocess.Popen(["python3", "/root/passivbot_configs/eth.py"])
        ada = subprocess.Popen(["python3", "/root/passivbot_configs/ada.py"])
        doge = subprocess.Popen(["python3", "/root/passivbot_configs/doge.py"])

        withdrawAvailable = float(client.futures_account_balance()[9]["withdrawAvailable"])
        balance = float(client.futures_account_balance()[9]["balance"])
        ratio = withdrawAvailable / balance
        print(ratio)

        # Read in the file
        with open('/root/passivbot_configs/variables.json', 'r') as f:
            data = f.read()
        d = json.loads(data)

        if 1 > ratio > 0.75 and d['time_to_cool_down'] != 60:
            d['time_to_cool_down'] = 60

            with open('/root/passivbot_configs/variables.json', 'w') as f:
                json.dump(d, f)

            eth.kill()
            ada.kill()
            doge.kill()
            eth
            ada
            doge

        if 0.74 > ratio > 0.51 and d['time_to_cool_down'] != 120:
            d['time_to_cool_down'] = 120

            with open('/root/passivbot_configs/variables.json', 'w') as f:
                json.dump(d, f)

            eth.kill()
            ada.kill()
            doge.kill()
            eth
            ada
            doge

        if 0.51 > ratio > 0.33 and d['time_to_cool_down'] != 540:
            d['time_to_cool_down'] = 540

            with open('/root/passivbot_configs/variables.json', 'w') as f:
                json.dump(d, f)

            eth.kill()
            ada.kill()
            doge.kill()
            eth
            ada
            doge

        if 0.32 > ratio and d['time_to_cool_down'] != 43200:
            d['time_to_cool_down'] = 43200

            with open('/root/passivbot_configs/variables.json', 'w') as f:
                json.dump(d, f)

            eth.kill()
            ada.kill()
            doge.kill()
            eth
            ada
            doge

        time.sleep(time_to_wait_one_more_check)
    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
