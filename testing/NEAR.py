import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'NEARBUSD'
greed = variables['greed']
multiplier = variables['NEAR']['multiplier']
long_profit_percentage = variables['NEAR']['long_profit_percentage']
short_profit_percentage = variables['NEAR']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)