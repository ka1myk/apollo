import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "GMT"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['GMT']['multiplier']
long_profit_percentage = variables['GMT']['long_profit_percentage']
short_profit_percentage = variables['GMT']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)