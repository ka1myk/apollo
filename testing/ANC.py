import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

symbol = 'ANCBUSD'
greed = variables['greed']
multiplier = variables['ANC']['multiplier']
long_profit_percentage = variables['ANC']['long_profit_percentage']
short_profit_percentage = variables['ANC']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)