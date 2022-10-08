# TODO tradingview add various exchanges

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


def margin_create_buy():
    client.create_margin_order(symbol=symbol,
                               side='BUY',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


def margin_create_sell():
    client.create_margin_order(symbol=symbol,
                               side='SELL',
                               type='MARKET',
                               quoteOrderQty=get_quoteOrderQty(symbol))


if strategy == "coinglass":
    #1m=9, 5m=3, 15m=10, 30m=11, 4h=1, 12h=4, 90d=18

    headers = {'coinglassSecret': '50f90ddcd6a8437992431ab0f1b698c1'}
    eth_url = requests.get(
        "https://open-api.coinglass.com/api/pro/v1/futures/liquidation/detail/chart?symbol=ETH&timeType=3",
        headers=headers)
    text = eth_url.text
    eth_data = json.loads(text)

    btc_url = requests.get(
        "https://open-api.coinglass.com/api/pro/v1/futures/liquidation/detail/chart?symbol=BTC&timeType=3",
        headers=headers)
    text = btc_url.text
    btc_data = json.loads(text)

    print(float(eth_data['data'][89]['buyVolUsd']))
    print(float(btc_data['data'][89]['buyVolUsd']))

    print(float(eth_data['data'][89]['sellVolUsd']))
    print(float(btc_data['data'][89]['sellVolUsd']))

if strategy == "tradingview":
    INTERVAL_1_HOUR = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_1_HOUR
    )

    INTERVAL_4_HOURS = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_4_HOURS
    )

    if INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"] in ("STRONG_BUY", "BUY") and \
            INTERVAL_4_HOURS.get_analysis().summary["RECOMMENDATION"] in ("STRONG_BUY", "BUY"):
        margin_create_buy()
    else:
        margin_create_sell()

if strategy == "cryptometer":
    # https://www.cryptometer.io/api-doc/
    print("TBD")

if strategy == "cryptosignal":
    # https://github.com/CryptoSignal/Crypto-Signal
    print("TBD")

if strategy == "coingecko":
    # https://github.com/man-c/pycoingecko
    # https://www.coingecko.com/en/api/documentation
    print("TBD")

if strategy == "polygon":
    # https://polygon.io/
    print("TBD")

if strategy == "taapi":
    # https://taapi.io/
    print("TBD")