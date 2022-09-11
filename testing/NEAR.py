import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "NEAR"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['NEAR']['multiplier']
long_profit_percentage = variables['NEAR']['long_profit_percentage']
short_profit_percentage = variables['NEAR']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)