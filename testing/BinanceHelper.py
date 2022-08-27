import math
import json
from binance.client import Client


class BinanceHelper(object):

    def do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage):

        with open('api-keys.json') as p:
            creds = json.load(p)
        client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

        info = client.futures_exchange_info()

        def get_pricePrecision(pair):
            for x in info['symbols']:
                if x['symbol'] == pair:
                    return x['pricePrecision']

        def get_quantityPrecision(pair):
            for x in info['symbols']:
                if x['symbol'] == pair:
                    return x['quantityPrecision']

        def get_notional(pair):
            for x in info['symbols']:
                if x['symbol'] == pair:
                    for y in x['filters']:
                        if y['filterType'] == 'MIN_NOTIONAL':
                            return y['notional']

        def round_up(n, decimals=0):
            round_up_multiplier = 10 ** decimals
            return math.ceil(n * round_up_multiplier) / round_up_multiplier

        minNotional = round_up(
            float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
            get_quantityPrecision(symbol))

        client.futures_create_order(symbol=symbol,
                                    quantity=round(minNotional * multiplier * greed, get_quantityPrecision(symbol)),
                                    side='BUY',
                                    positionSide='LONG',
                                    type='MARKET')

        client.futures_create_order(symbol=symbol,
                                    quantity=round(minNotional * multiplier * greed, get_quantityPrecision(symbol)),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='MARKET')

        long_positionAmt = abs(float(client.futures_position_information(symbol=symbol)[1]["positionAmt"]))
        long_take_profit_price = round_up(
            float(client.futures_position_information(symbol=symbol)[1]["entryPrice"]) * long_profit_percentage,
            get_pricePrecision(symbol))

        short_positionAmt = abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]))
        short_take_profit_price = round_up(
            float(client.futures_position_information(symbol=symbol)[2]["entryPrice"]) * short_profit_percentage,
            get_pricePrecision(symbol))

        client.futures_cancel_all_open_orders(symbol=symbol)

        if float(long_positionAmt) != 0:
            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_positionAmt * 0.8, get_quantityPrecision(symbol)),
                                        price=round(long_take_profit_price * 1, get_pricePrecision(symbol)),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(long_take_profit_price * 1.005, get_pricePrecision(symbol)),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(long_take_profit_price * 1.01, get_pricePrecision(symbol)),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(long_take_profit_price * 1.015, get_pricePrecision(symbol)),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(long_take_profit_price * 1.02, get_pricePrecision(symbol)),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

        if float(short_positionAmt) != 0:
            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_positionAmt * 0.8, get_quantityPrecision(symbol)),
                                        price=round(short_take_profit_price * 1, get_pricePrecision(symbol)),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(short_take_profit_price * 0.995, get_pricePrecision(symbol)),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(short_take_profit_price * 0.99, get_pricePrecision(symbol)),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(short_take_profit_price * 0.985, get_pricePrecision(symbol)),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_positionAmt * 0.05, get_quantityPrecision(symbol)),
                                        price=round(short_take_profit_price * 0.98, get_pricePrecision(symbol)),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )