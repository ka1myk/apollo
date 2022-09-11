import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "1000SHIB"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['1000SHIB']['multiplier']
long_profit_percentage = variables['1000SHIB']['long_profit_percentage']
short_profit_percentage = variables['1000SHIB']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)