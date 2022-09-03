import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'XRPBUSD'
greed = variables['greed']
multiplier = variables['XRP']['multiplier']
long_profit_percentage = variables['XRP']['long_profit_percentage']
short_profit_percentage = variables['XRP']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)