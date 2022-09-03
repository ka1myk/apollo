import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'DOGEBUSD'
greed = variables['greed']
multiplier = variables['DOGE']['multiplier']
long_profit_percentage = variables['DOGE']['long_profit_percentage']
short_profit_percentage = variables['DOGE']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)