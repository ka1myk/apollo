import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "BTC"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['BTC']['multiplier']
long_profit_percentage = variables['BTC']['long_profit_percentage']
short_profit_percentage = variables['BTC']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)