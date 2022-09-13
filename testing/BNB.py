import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "BNB"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['BNB']['multiplier']
long_profit_percentage = variables['BNB']['long_profit_percentage']
short_profit_percentage = variables['BNB']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)