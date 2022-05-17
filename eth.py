from decimal import Decimal
from binance.client import Client
import requests, json, time
from variables import time_to_create_order, time_to_wait_one_more_check, time_to_cool_down, time_to_create_gs_order

with open('/root/passivbot/api-keys.json') as p:
    creds = json.load(p)

client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

while True:
    try:
        headers = {'coinglassSecret': '50f90ddcd6a8437992431ab0f1b698c1'}
        url = requests.get(
            "https://open-api.coinglass.com/api/pro/v1/futures/liquidation/detail/chart?symbol=ETH&timeType=9",
            headers=headers)
        text = url.text
        data = json.loads(text)

        long_signal = float(data['data'][90]['buyVolUsd'])
        if long_signal > 40000:
            print('fire_long')

            priceForOpenLongOrder = format(Decimal(client.futures_coin_ticker(symbol='ETHUSD_PERP')[0]['lastPrice']),
                                           '.2f')

            client.futures_create_order(symbol='ETHBUSD', side='BUY', positionSide='LONG', type='LIMIT', quantity=0.003,
                                        timeInForce='GTX', price=priceForOpenLongOrder, recvWindow=20000)

            # priceForCloseLongOrder = format(
            #     Decimal(client.futures_position_information(symbol='ETHBUSD')[1]['entryPrice']), '.2f')
            # amtForCloseLongOrder = Decimal(client.futures_position_information(symbol='ETHBUSD')[1]['positionAmt'])
            #
            # print("priceForCloseLongOrder", priceForCloseLongOrder)
            # print("amtForCloseLongOrder", amtForCloseLongOrder)
            #
            # client.futures_create_order(symbol='ETHBUSD', side='SELL', positionSide='LONG', type='LIMIT',
            #                             quantity=amtForCloseLongOrder,
            #                             timeInForce='GTX', price=priceForCloseLongOrder)

            time.sleep(time_to_cool_down)

        short_signal = float(data['data'][90]['sellVolUsd'])
        if short_signal > 40000:
            print('fire_short')

            # open short order and close short order#
            priceForOpenShortOrder = format(Decimal(client.futures_coin_ticker(symbol='ETHUSD_PERP')[0]['lastPrice']),
                                            '.2f')

            client.futures_create_order(symbol='ETHBUSD', side='SELL', positionSide='SHORT', type='LIMIT',
                                        quantity=0.004,
                                        timeInForce='GTX', price=priceForOpenShortOrder, recvWindow=20000)

            # priceForCloseShortOrder = format(
            #     Decimal(client.futures_position_information(symbol='ETHBUSD')[2]['entryPrice']), '.2f')
            # amtForCloseShortOrder = format(
            #     abs(Decimal(client.futures_position_information(symbol='ETHBUSD')[2]['positionAmt'])))
            #
            # print("priceForCloseShortOrder", priceForCloseShortOrder)
            # print("amtForCloseShortOrder", amtForCloseShortOrder)
            #
            # client.futures_create_order(symbol='ETHBUSD', side='BUY', positionSide='SHORT', type='LIMIT',
            #                             quantity=amtForCloseShortOrder,
            #                             timeInForce='GTX', price=priceForCloseShortOrder)

            # -----------------------------------#

            time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
