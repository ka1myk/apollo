import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "GALA"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['GALA']['multiplier']
long_profit_percentage = variables['GALA']['long_profit_percentage']
short_profit_percentage = variables['GALA']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)