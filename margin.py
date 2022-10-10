# TODO tradingview add various exchanges
import time
import urllib

import requests
import json
import argparse
from binance.client import Client
from binance.helpers import round_step_size

from tradingview_ta import TA_Handler, Interval, Exchange

with open('variables.json') as v:
    variables = json.load(v)

parser = argparse.ArgumentParser()

parser.add_argument('--pair', type=str, required=True)
parser.add_argument('--strategy', type=str, required=True)

args = vars(parser.parse_args())

symbol = args['pair']
strategy = args['strategy']

client = Client(variables['binance_01']['key'], variables['binance_01']['secret'])

info = client.get_symbol_info(symbol)
price = client.get_avg_price(symbol=symbol)['price']


def set_greed():
    if float(client.get_margin_account()['totalAssetOfBtc']) < 0.1:
        greed = 1
    else:
        greed = round(float(client.get_margin_account()['totalAssetOfBtc']) / 0.1)
    return greed


def get_notional(symbol):
    for y in info['filters']:
        if y['filterType'] == 'MIN_NOTIONAL':
            return y['minNotional']


def get_price_precision(symbol):
    n = len(str(get_rounded_price(symbol, price)).split(".")[1])
    return n


def get_tick_size(symbol):
    for y in info['filters']:
        if y['filterType'] == 'PRICE_FILTER':
            return y['tickSize']


def get_rounded_price(symbol: str, price: float) -> float:
    return round_step_size(price, get_tick_size(symbol))


def get_quoteOrderQty(symbol: str) -> float:
    return float(get_notional(symbol)) * set_greed()


def margin_create_market_buy():
    client.create_margin_order(symbol=symbol,
                               side='BUY',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


def margin_create_market_sell():
    client.create_margin_order(symbol=symbol,
                               side='SELL',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


def margin_create_limit_sell():
    avg_price_with_sell_profit_and_precision = round(float(price) * float(1.01),
                                                     get_price_precision(symbol))

    quantity = round(float(get_notional(symbol)) * 1.01 / float(price), 4)

    client.create_margin_order(symbol=symbol, side='SELL', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_sell_profit_and_precision)


def margin_create_limit_buy():
    avg_price_with_buy_profit_and_precision = round(float(price) * float(0.99),
                                                    get_price_precision(symbol))

    quantity = round(float(get_notional(symbol)) * 1.01 / float(price), 4)

    client.create_margin_order(symbol=symbol, side='BUY', type='LIMIT', timeInForce="GTC",
                               quantity=quantity,
                               price=avg_price_with_buy_profit_and_precision)


if strategy == "coinglass":
    # 1m=9, 5m=3, 15m=10, 30m=11, 4h=1, 12h=4, 90d=18 in docs
    # 0, 3, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 19 - no response
    # 1+, 2, 4+, 9+, 10+, 11+, 18+ - get 200 ok
    # 1 {'buyVolUsd': 2117337.962561, 'sellVolUsd': 3730660.27687, 'createTime': 1663948800000 }
    # 2 [{'buyVolUsd': 260.00453, 'sellVolUsd': 58532.86362, 'createTime': 1664928000000,}
    # ~ 4 days ago 1665254300

    headers = {'coinglassSecret': '50f90ddcd6a8437992431ab0f1b698c1'}
    eth_url = requests.get(
        "https://open-api.coinglass.com/api/pro/v1/futures/liquidation/detail/chart?symbol=ETH&timeType=11",
        headers=headers)
    text = eth_url.text
    eth_data = json.loads(text)

    btc_url = requests.get(
        "https://open-api.coinglass.com/api/pro/v1/futures/liquidation/detail/chart?symbol=BTC&timeType=11",
        headers=headers)
    text = btc_url.text
    btc_data = json.loads(text)

    if float(eth_data['data'][89]['buyVolUsd']) + float(btc_data['data'][89]['sellVolUsd']) > float(
            btc_data['data'][89]['buyVolUsd']) + float(eth_data['data'][89]['sellVolUsd']):
        margin_create_market_sell()
        margin_create_limit_buy()
    else:
        margin_create_market_buy()
        margin_create_limit_sell()

if strategy == "tradingview":
    INTERVAL_30_MINUTES = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_30_MINUTES
    )

    INTERVAL_1_HOUR = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_1_HOUR
    )

    if INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"] in ("STRONG_BUY", "BUY") and \
            INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"] in ("STRONG_BUY", "BUY"):
        margin_create_market_buy()
        margin_create_limit_sell()

    if INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"] in ("STRONG_SELL", "SELL") and \
            INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"] in ("STRONG_SELL", "SELL"):
        margin_create_market_sell()
        margin_create_limit_buy()

if strategy == "cryptometer":
    # https://www.cryptometer.io/api-doc/
    # MACD
    # RSI
    # ATR
    # PSAR
    # EMA
    # SMA
    # CCI
    # api = 1161x8cbc9366T614xy23G3s1006S2TNQf6b6He7

    cryptometer_key = "1161x8cbc9366T614xy23G3s1006S2TNQf6b6He7"
    eth_url = requests.get(
        "https://api.cryptometer.io/open-interest/?market_pair=ethbusd&e=binance_futures&api_key=" + str(
            cryptometer_key))
    text = eth_url.text
    eth_data = json.loads(text)

    btc_url = requests.get(
        "https://api.cryptometer.io/open-interest/?market_pair=btcbusd&e=binance_futures&api_key=" + str(
            cryptometer_key))
    text = btc_url.text
    btc_data = json.loads(text)

    print(float(eth_data["data"][0]["open_interest"]))
    print(float(btc_data["data"][0]["open_interest"]))

if strategy == "taapi":
    # https://taapi.io/
    taapi_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM0NDRhM2ZmYzVhOGFkZmVjMWM5NGRkIiwiaWF0IjoxNjY1NDE5ODUxLCJleHAiOjMzMTY5ODgzODUxfQ.piZ025xlPHtQitPzFJbWXHzLQXZ_XVGEAQu-9TnK77g"

    # Define indicator
    indicator = "rsi"

    # Define endpoint
    endpoint = f"https://api.taapi.io/{indicator}"

    # Define a parameters dict for the parameters to be sent to the API
    parameters_1 = {
        'secret': taapi_key,
        'exchange': 'binance',
        'symbol': 'BTC/USDT',
        'interval': '30m'
    }

    parameters_2 = {
        'secret': taapi_key,
        'exchange': 'binance',
        'symbol': 'ETH/USDT',
        'interval': '30m'
    }

    # Send get request and save the response as response object
    response_1 = requests.get(url=endpoint, params=parameters_1)
    time.sleep(16)
    response_2 = requests.get(url=endpoint, params=parameters_2)


    # Extract data in json format
    result_1 = response_1.json()
    result_2 = response_2.json()

    # Print result
    print(result_1)
    print(result_2)

