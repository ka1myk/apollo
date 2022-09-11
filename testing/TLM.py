import BinanceHelper
import json

with open('variables.json') as v:
    variables = json.load(v)

coin = "TLM"
currency = variables['currency']
symbol = coin + currency
greed = variables['greed']
multiplier = variables['TLM']['multiplier']
long_profit_percentage = variables['TLM']['long_profit_percentage']
short_profit_percentage = variables['TLM']['short_profit_percentage']

BinanceHelper.BinanceHelper.do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage)