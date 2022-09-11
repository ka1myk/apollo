import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "AUCTION"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['AUCTION']['multiplier']
long_profit_percentage = variables['AUCTION']['long_profit_percentage']
short_profit_percentage = variables['AUCTION']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)