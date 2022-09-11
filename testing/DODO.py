import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "DODO"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['DODO']['multiplier']
long_profit_percentage = variables['DODO']['long_profit_percentage']
short_profit_percentage = variables['DODO']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)