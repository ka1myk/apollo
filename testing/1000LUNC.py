import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = '1000LUNCBUSD'
greed = variables['greed']
multiplier = variables['1000LUNC']['multiplier']
long_profit_percentage = variables['1000LUNC']['long_profit_percentage']
short_profit_percentage = variables['1000LUNC']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)