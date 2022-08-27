import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'LINKBUSD'
greed = variables['greed']
multiplier = variables['LINK']['multiplier']
long_profit_percentage = variables['LINK']['long_profit_percentage']
short_profit_percentage = variables['LINK']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)