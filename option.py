import json

from binance.client import BaseClient
from binance.client import Client

BaseClient.OPTIONS_URL = 'https://eapi.binance.{}/eapi'

with open('variables.json') as v:
    variables = json.load(v)

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])


print(client.options_mark_price())

