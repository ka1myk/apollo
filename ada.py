from tradingview_ta import TA_Handler, Interval, Exchange
from binance.client import Client
import requests, json, time

with open('api-keys.json') as p:
    creds = json.load(p)

client = Client(creds['binance_01']['key'], creds['binance_01']['secret'])

ADABUSDPERP_INTERVAL_1_MINUTE = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)

ADABUSDPERP_INTERVAL_5_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_5_MINUTES
)

ADABUSDPERP_INTERVAL_15_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_15_MINUTES
)

ADABUSDPERP_INTERVAL_30_MINUTES = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_30_MINUTES
)

ADABUSDPERP_INTERVAL_1_HOUR = TA_Handler(
    symbol="ADABUSDPERP",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_HOUR
)

while True:

    try:

        with open('variables.json') as v:
            variables = json.load(v)

        symbol = 'ADABUSD'
        pricePrecision = 4
        min_amount = 10

        time_to_wait_one_more_check = variables['time_to_wait_one_more_check']
        time_to_cool_down = variables['time_to_cool_down']
        long_profit_percent = variables['long_profit_percent']
        short_profit_percent = variables['short_profit_percent']
        leverage = variables['leverage']
        multiplier = variables['multiplier']

        if (
                (
                        ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                        and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_BUY", "BUY")
                )

                or

                (
                        ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                        and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                        in ("STRONG_SELL", "SELL")
                )

        ):
            time.sleep(time_to_wait_one_more_check)

            if (

                    (
                            ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                            and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_BUY", "BUY")
                    )

                    or

                    (
                            ADABUSDPERP_INTERVAL_1_MINUTE.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_5_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_15_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_30_MINUTES.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                            and ADABUSDPERP_INTERVAL_1_HOUR.get_analysis().summary["RECOMMENDATION"]
                            in ("STRONG_SELL", "SELL")
                    )

            ):
                # create open long order market #
                client.futures_create_order(symbol=symbol,
                                            side='BUY',
                                            positionSide='LONG',
                                            type='MARKET',
                                            leverage=leverage,
                                            quantity=min_amount * multiplier)

                # create open short order market #
                client.futures_create_order(symbol=symbol,
                                            side='SELL',
                                            positionSide='SHORT',
                                            type='MARKET',
                                            leverage=leverage,
                                            quantity=min_amount * multiplier)

                # do not modify! #
                time.sleep(1.5)

                # cancel all orders by symbol to create new #
                client.futures_cancel_all_open_orders(symbol=symbol)

                # create close long order with profit long_profit_percent #
                client.futures_create_order(symbol=symbol, side='SELL', positionSide='LONG', type='LIMIT',
                                            timeInForce='GTC',
                                            price=round(abs(float(
                                                client.futures_position_information(symbol=symbol)[1].get(
                                                    'entryPrice'))) * long_profit_percent,
                                                        pricePrecision),
                                            quantity=abs(
                                                float(client.futures_position_information(symbol=symbol)[1].get(
                                                    'positionAmt'))))

                # create close long order with profit short_profit_percent #
                client.futures_create_order(symbol=symbol, side='BUY', positionSide='SHORT', type='LIMIT',
                                            timeInForce='GTC',
                                            price=round(abs(float(
                                                client.futures_position_information(symbol=symbol)[2].get(
                                                    'entryPrice'))) * short_profit_percent,
                                                        pricePrecision),
                                            quantity=abs(
                                                float(client.futures_position_information(symbol=symbol)[2].get(
                                                    'positionAmt'))))

                time.sleep(time_to_cool_down)

    except Exception as e:
        print("Function errored out!", e)
        print("Retrying ... ")
