import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "LDO"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['LDO']['multiplier']
long_profit_percentage = variables['LDO']['long_profit_percentage']
short_profit_percentage = variables['LDO']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)