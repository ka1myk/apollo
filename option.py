import json

from binance.client import Client

OPTIONS_URL = 'https://eapi.binance.{}/eapi'

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])

client.options_account_info()