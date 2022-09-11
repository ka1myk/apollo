import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "ETH"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['ETH']['multiplier']
long_profit_percentage = variables['ETH']['long_profit_percentage']
short_profit_percentage = variables['ETH']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)