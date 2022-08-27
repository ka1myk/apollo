import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'APEBUSD'
greed = variables['greed']
multiplier = variables['APE']['multiplier']
long_profit_percentage = variables['APE']['long_profit_percentage']
short_profit_percentage = variables['APE']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)