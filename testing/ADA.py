import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'ADABUSD'
greed = variables['greed']
multiplier = variables['ADA']['multiplier']
long_profit_percentage = variables['ADA']['long_profit_percentage']
short_profit_percentage = variables['ADA']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)