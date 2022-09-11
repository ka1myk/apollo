import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "MATIC"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['MATIC']['multiplier']
long_profit_percentage = variables['MATIC']['long_profit_percentage']
short_profit_percentage = variables['MATIC']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)