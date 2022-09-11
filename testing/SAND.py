import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "SAND"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['SAND']['multiplier']
long_profit_percentage = variables['SAND']['long_profit_percentage']
short_profit_percentage = variables['SAND']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)