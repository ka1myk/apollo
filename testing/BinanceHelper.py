import math
import json
from binance.client import Client
from binance.helpers import round_step_size


class BinanceHelper:

    def do_profit(symbol, greed, multiplier, long_profit_percentage, short_profit_percentage):

        with open('api-keys.json') as p:
            creds = json.load(p)
        client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

        info = client.futures_exchange_info()

        def get_quantity_precision(pair):
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

        def get_tick_size(symbol: str) -> float:
            for symbol_info in info['symbols']:
                if symbol_info['symbol'] == symbol:
                    for symbol_filter in symbol_info['filters']:
                        if symbol_filter['filterType'] == 'PRICE_FILTER':
                            return float(symbol_filter['tickSize'])

        def get_rounded_price(symbol: str, price: float) -> float:
            return round_step_size(price, get_tick_size(symbol))

        min_notional = round_up(
            float(get_notional(symbol)) / float(client.futures_mark_price(symbol=symbol)["markPrice"]),
            get_quantity_precision(symbol))

        client.futures_create_order(symbol=symbol,
                                    quantity=round(min_notional * multiplier * greed, get_quantity_precision(symbol)),
                                    side='BUY',
                                    positionSide='LONG',
                                    type='MARKET')

        client.futures_create_order(symbol=symbol,
                                    quantity=round(min_notional * multiplier * greed, get_quantity_precision(symbol)),
                                    side='SELL',
                                    positionSide='SHORT',
                                    type='MARKET')

        long_position_amt = abs(float(client.futures_position_information(symbol=symbol)[1]["positionAmt"]))
        long_take_profit_price = get_rounded_price(symbol, float(
            client.futures_position_information(symbol=symbol)[1]["entryPrice"]) * long_profit_percentage)

        short_position_amt = abs(float(client.futures_position_information(symbol=symbol)[2]["positionAmt"]))
        short_take_profit_price = get_rounded_price(symbol, float(
            client.futures_position_information(symbol=symbol)[2]["entryPrice"]) * short_profit_percentage)

        client.futures_cancel_all_open_orders(symbol=symbol)

        if float(long_position_amt) != 0:
            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_position_amt * 0.6, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, long_take_profit_price * 1),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, long_take_profit_price * 1.005),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, long_take_profit_price * 1.01),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, long_take_profit_price * 1.015),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(long_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, long_take_profit_price * 1.02),
                                        side='SELL',
                                        positionSide='LONG',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )

        if float(short_position_amt) != 0:
            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_position_amt * 0.6, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, short_take_profit_price * 1),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, short_take_profit_price * 0.995),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, short_take_profit_price * 0.99),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, short_take_profit_price * 0.985),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
            client.futures_create_order(symbol=symbol,
                                        quantity=round(short_position_amt * 0.1, get_quantity_precision(symbol)),
                                        price=get_rounded_price(symbol, short_take_profit_price * 0.98),
                                        side='BUY',
                                        positionSide='SHORT',
                                        type='LIMIT',
                                        timeInForce="GTC"
                                        )
