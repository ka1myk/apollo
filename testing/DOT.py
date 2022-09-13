import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "DOT"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['DOT']['multiplier']
long_profit_percentage = variables['DOT']['long_profit_percentage']
short_profit_percentage = variables['DOT']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)