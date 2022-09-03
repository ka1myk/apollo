import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'LTCBUSD'
greed = variables['greed']
multiplier = variables['LTC']['multiplier']
long_profit_percentage = variables['LTC']['long_profit_percentage']
short_profit_percentage = variables['LTC']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)