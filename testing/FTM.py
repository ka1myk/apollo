import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "FTM"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['FTM']['multiplier']
long_profit_percentage = variables['FTM']['long_profit_percentage']
short_profit_percentage = variables['FTM']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)